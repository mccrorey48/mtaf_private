import contextlib
import json
import re
import sys
from datetime import datetime, timedelta
from behave.__main__ import main
from pymongo import MongoClient
from mtaf import mtaf_logging
from mtaf.fake_detector import FakeDetector
from mtaf.user_exception import UserException as Ux
from mtaf.trace import Trace
from mtaf.prune_db import prune_db
import argparse
from os import path, getenv, mkdir
from shutil import copyfile
from bson.binary import Binary
import six
if six.PY3:
    from io import StringIO
else:
    from cStringIO import StringIO

log = mtaf_logging.get_logger('mtaf.run_features')
mtaf_log_dir = getenv('MTAF_LOG_DIR', './log')
browser_log = ''


@contextlib.contextmanager
def capture():
    import sys
    oldout, olderr = sys.stdout, sys.stderr
    out = []
    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


@Trace(log)
def run_features(config):
    global browser_log
    # make sure the tmp directory exists so we can put temporary files there
    try:
        mkdir('tmp')
    except OSError:
        pass
    sys.argv = [re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])]
    sys.argv.append('-D')
    sys.argv.append('portal_server=%s' % config['portal_server'])
    sys.argv.append('-D')
    sys.argv.append('user_scope=%s' % config['user_scope'])
    sys.argv.append('--tags=%s' % config['user_scope'])
    if config['run_tags']:
        sys.argv.append('--tags=%s' % config['run_tags'])
    if config['stop']:
        sys.argv.append('--stop')
    sys.argv.append('-k')
    sys.argv.append('-f')
    sys.argv.append('json.pretty')
    sys.argv.append(config['features_dir'])
    start_time = datetime.now()
    with capture() as out:
        main()

    # save the output of behave (json test results plus plain text summary at the end)
    # for reference and debugging
    with open('tmp/main.out', 'w') as f:
        f.write(out[0])

    # - go through the list of executed step and substep names
    # - substep names are CSV format: name, result, duration
    # - for each executed step, create a dictionary {"name": <step name>, "substeps": []}
    # - for each step that has substeps, append the substep names and data to the "substeps" attribute for that step
    # - append the step to the printed_steps array
    with open('tmp/steps.txt', 'r') as f:
        executed_steps = f.read()
    printed_steps = []
    current_step = None
    for line in executed_steps.strip().split('\n'):
        if len(line.split(' = ')) != 2:
            continue
        (_type, name) = line.split(' = ')
        if _type == 'step':
            if current_step is not None:
                printed_steps.append(current_step)
            current_step = {"name": name, "substeps": []}
        elif _type == 'substep' and current_step is not None:
            splitname = name.split(',')
            name = ' '.join(splitname[:-2])
            substep = {
                "name": name,
                "text": rm_view_prefix(name),
                "keyword": "Substep",
                "status": splitname[-2],
                "duration": splitname[-1]
            }
            current_step["substeps"].append(substep)
        elif _type == 'screenshot' and current_step is not None:
            current_step['screenshot'] = name
        elif _type == 'browser_log':
            browser_log = name
    if current_step is not None:
        printed_steps.append(current_step)

    # - save the json part of the behave output in the file json_repr.json
    # - create "data" (array of features defined, whether executed or not) from the json
    json_repr = '\n'.join(out[0][:out[0].rindex(']') + 1].split('\n'))
    with open('tmp/json_repr.json', 'w') as f:
        f.write(json_repr)
    data = json.loads(json_repr)
    if len(data):
        data[0]["start_time"] = start_time.strftime("%X")
        data[0]["start_date"] = start_time.strftime("%x")

    # "data" includes both executed and skipped steps, organized by feature and scenario
    # but does not include substeps; loop through "data" and "printed_steps" simultaneously
    # and when a step in "printed_steps" has substeps, add them to "data"
    # (if the two data sets don't produce the same sequence of steps, raise an exception
    # because something isn't working right)
    for feature in data:
        # six.print_(feature['name'])
        for element in feature["elements"]:
            # six.print_('  ' + element['name'])
            if element["keyword"] == "Scenario":
                new_steps = []
                for step in element["steps"]:
                    if "result" in step:
                        # six.print_('    ' + step['name'])
                        # if it gets to here, the step was executed and should be on the printed_steps list
                        if len(printed_steps) == 0:
                            raise Ux("Error processing new_steps list, printed_steps empty")
                        printed_step = printed_steps.pop(0)
                        if printed_step["name"] != step["name"]:
                            raise Ux("Error processing new_steps list, %s != %s" % (printed_step["name"], step["name"]))
                        step["substeps"] = printed_step["substeps"]
                        if 'screenshot' in printed_step:
                            step["screenshot"] = printed_step["screenshot"]
                    # else:
                    #     six.print_('    ' + step['name'] + ' (skipped)')
                    new_steps.append(step)
                element["steps"] = new_steps
    output = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    with open('tmp/output.json', 'w') as f:
        f.write(output)
    copyfile(path.join(mtaf_log_dir, 'mtaf_info.log'), path.join(mtaf_log_dir, 'mtaf_info_copy.log'))
    return data


def rm_view_prefix(step_name):
    step_re = re.compile('\s*(\[\s*([^]]*\S)\s*\]\s*)?\s*(.*\S)\s*')
    m = step_re.match(step_name)
    if m:
        return m.group(3)
    else:
        return step_name


re_name = re.compile('(?P<date>\S+) (?P<time>[^.]+)\.(?P<ms>\d+).*(?P<type>feature|scenario|step)\.name: (?P<name>.*)')


class StepInfo:
    def __init__(self, fname):
        self.fname = fname
        self._feature = None
        self._scenario = None
        self.f = open(self.fname)

    def parse(self, feature_text, scenario_text, step_text):
        while True:
            line = self.f.readline()
            log.debug("StepInfo.parse(): line = '%s'" % line.strip())
            if not line:
                break
            m = re_name.match(line)
            if not m:
                continue
            if m.group('type') == 'feature':
                self._feature = m.group('name')
            elif m.group('type') == 'scenario':
                self._scenario = m.group('name')
            else:
                if self._feature != feature_text:
                    raise Ux('expected feature name %s, got %s' % (feature_text, self._feature))
                if self._scenario != scenario_text:
                    raise Ux('expected scenario name %s, got %s' % (scenario_text, self._scenario))
                _step = rm_view_prefix(m.group('name'))
                if _step != step_text:
                    raise Ux('expected step name %s, got %s' % (step_text, _step))
                yield m.group('date'), m.group('time')


def new_step_status(old_status, has_passes, has_fails, has_fakes):
    if old_status == 'failed':
        return 'failed'
    elif has_passes is False and has_fails is False and has_fakes is False:
        return old_status
    elif old_status == 'skipped':
        raise Ux('unexpected has_x == True in skipped step')
    elif has_fails:
        return 'failed'
    elif has_fakes:
        return 'incomplete'
    else:
        if old_status == 'passed' or old_status == 'fake':
            return 'passed'


def new_status(has_passes=False, has_fails=False, has_fakes=False, has_skips=False, has_incompletes=False):
    if has_fails:
        return 'failed'
    if has_passes is True and has_fakes is False and has_skips is False and has_incompletes is False:
        return 'passed'
    if has_passes is False and has_fakes is False and has_skips is True and has_incompletes is False:
        return 'skipped'
    # if has_passes is False and has_fakes is True and has_skips is False and has_incompletes is False:
    if has_passes is False and has_fakes is True and has_incompletes is False:
        return 'fake'
    if has_fakes or has_incompletes or has_skips:
            return 'incomplete'
    return 'passed'


def write_result_to_db(_args, configuration, _fake_detector, _features):
    six.print_('writing to db_name %s, server %s:' % (_args.db_name, _args.server))
    client = MongoClient(_args.server)
    db = client[_args.db_name]
    if len(_features) and 'start_time' in _features[0] and 'start_date' in _features[0]:
        start_datetime = datetime.strptime("%s %s" % (_features[0]['start_date'], _features[0]['start_time']), '%x %X')
    else:
        start_datetime = datetime.now()
    test_start = {
        'app': 'eConsole',
        'build': '',
        'configuration': configuration,
        'environment': configuration['portal_server'],
        'fail_count': 0,
        'skip_count': 0,
        'pass_count': 0,
        'status': '',
        'test_class': _args.test_class,
        'time': start_datetime.strftime('%X'),
        'date': start_datetime.strftime('%x'),
        'version': '1.x'
    }
    start_id = db['test_starts'].insert_one(test_start).inserted_id
    fail_count = 0
    pass_count = 0
    skip_count = 0
    if _args.json_file:
        info_filename = path.join(mtaf_log_dir, 'mtaf_info_copy.log')
    else:
        info_filename = path.join(mtaf_log_dir, 'mtaf_info.log')
    stepinfo = StepInfo(info_filename)
    last_step_duration = 0
    for iter_num, feature in enumerate(_features):
        feature_has_skips = False
        feature_has_fakes = False
        feature_has_fails = False
        feature_has_known_bug = False
        feature_has_passes = False
        feature_has_incompletes = False
        feature['start_id'] = start_id
        feature['test_class'] = _args.test_class
        feature['text'] = feature['name']
        del feature['name']
        feature['order'] = iter_num
        feature['scenarios'] = []
        feature['duration'] = 0.0
        for element in feature['elements']:
            if element['keyword'] != 'Background':
                feature['scenarios'].append(element)
        for scenario_index, scenario in enumerate(feature['scenarios']):
            scenario_has_skips = False
            scenario_has_fakes = False
            scenario_has_fails = False
            scenario_has_passes = False
            scenario_has_incompletes = False
            scenario['text'] = scenario['name']
            scenario['status'] = 'passed'
            del scenario['name']
            if 'tags' not in scenario.keys():
                scenario['tags'] = []
            scenario['duration'] = 0.0
            for step_index, step in enumerate(scenario['steps']):
                step['text'] = rm_view_prefix(step['name'])
                step_has_fails = False
                step_has_passes = False
                step_has_fakes = False
                if 'result' not in step:
                    # if 'result' is not in step, the step was skipped, either because it belongs
                    # to a scenario that was skipped (because it didn't have the right tag)
                    # or a previous step in the current scenario failed
                    step['status'] = 'skipped'
                    scenario_has_skips = True
                    step['duration'] = 0.0
                    start_datetime += timedelta(seconds=last_step_duration)
                else:
                    step['status'] = step['result']['status']
                    step['duration'] = step['result']['duration']
                    _date, _time = stepinfo.parse(feature['text'], scenario['text'], step['text']).next()
                    if "substeps" in step:
                        for substep in step["substeps"]:
                            _date, _time = stepinfo.parse(feature['text'], scenario['text'], substep['text']).next()
                            start_datetime = datetime.strptime("%s %s" % (_date, _time), '%x %X')
                            substep['time'] = start_datetime.strftime('%X')
                            substep['date'] = start_datetime.strftime('%x')
                            if _fake_detector.match(substep["name"]):
                                substep['status'] = 'fake'
                                step_has_fakes = True
                            elif substep['status'] == 'failed':
                                step_has_fails = True
                            elif substep['status'] == 'passed':
                                step_has_passes = True
                            else:
                                raise Ux("non-fake substep status not passed or failed")

                    if _fake_detector.match(step['name']):
                        step['status'] = 'fake'
                    step['status'] = new_step_status(step['status'], step_has_passes, step_has_fails, step_has_fakes)
                    if step['status'] == 'incomplete':
                        scenario_has_incompletes = True
                    elif step['status'] == 'fake':
                        scenario_has_fakes = True
                    elif step['status'] == 'failed':
                        scenario_has_fails = True
                        if 'screenshot' in step:
                            with open(step['screenshot'], 'rb') as f:
                                bin_data = StringIO(f.read())
                                step['screenshot_id'] = db['screenshots'].insert_one(
                                    {'screenshot': Binary(bin_data.getvalue())}).inserted_id
                    else:
                        scenario_has_passes = True
                    if 'error_message' in step['result']:
                        step['error_message'] = step['result']['error_message']
                    else:
                        step['error_message'] = ''
                    del step['result']
                    start_datetime = datetime.strptime("%s %s" % (_date, _time), '%x %X')
                    scenario['duration'] += step['duration']
                    feature['duration'] += step['duration']
                step['time'] = start_datetime.strftime('%X')
                step['date'] = start_datetime.strftime('%x')
                if step_index == 0:
                    scenario['time'] = start_datetime.strftime('%X')
                    scenario['date'] = start_datetime.strftime('%x')
                    if scenario_index == 0:
                        feature['time'] = start_datetime.strftime('%X')
                        feature['date'] = start_datetime.strftime('%x')
                del step['name']
                last_step_duration = step['duration']

            scenario['status'] = new_status(scenario_has_passes, scenario_has_fails, scenario_has_fakes,
                                            scenario_has_skips, scenario_has_incompletes)
            if scenario['status'] == 'failed':
                if 'known_bug' in scenario['tags'] + feature['tags']:
                    scenario['status'] = 'known_bug'
                    feature_has_known_bug = True
                else:
                    feature_has_fails = True
            elif scenario['status'] == 'skipped':
                feature_has_skips = True
            elif scenario['status'] == 'fake':
                feature_has_fakes = True
            elif scenario['status'] == 'passed':
                feature_has_passes = True
            elif scenario['status'] == 'incomplete':
                feature_has_incompletes = True

        del feature['elements']
        feature['status'] = new_status(feature_has_passes, feature_has_fails, feature_has_fakes,
                                       feature_has_skips, feature_has_incompletes)
        if feature['status'] == 'passed' and feature_has_known_bug:
            feature['status'] = 'known_bug'
        db['features'].insert_one(feature)
        # del feature['start_id']
        # six.print_(json.dumps(feature, sort_keys=True, indent=4, separators=(',', ':')))
    start_has_passes = False
    start_has_fails = False
    start_has_fakes = False
    start_has_skips = False
    start_has_incompletes = False
    start_has_known_bug = False
    for feature in _features:
        if feature['status'] == 'passed':
            pass_count += 1
            start_has_passes = True
        elif feature['status'] == 'skipped':
            skip_count += 1
            start_has_skips = True
        elif feature['status'] == 'failed':
            fail_count += 1
            start_has_fails = True
        elif feature['status'] == 'fake':
            start_has_fakes = True
        elif feature['status'] == 'incomplete':
            start_has_incompletes = True
        elif feature['status'] == 'known_bug':
            fail_count += 1
            start_has_known_bug = True
    start_result = new_status(start_has_passes, start_has_fails, start_has_fakes, start_has_skips, start_has_incompletes)
    if (start_result == 'passed' or start_result == 'skipped') and start_has_known_bug:
        start_result = 'known_bug'
    with open(browser_log, 'r') as f:
        log_data = f.read()
    db['test_starts'].find_one_and_update({"_id": start_id}, {'$set': {'pass_count': pass_count,
                                                                       'browser_log': log_data,
                                                                       'fail_count': fail_count,
                                                                       'skip_count': skip_count,
                                                                       'status': start_result}})
    # with open('tmp/screenshots.txt', 'r') as f:
    #     screenshots = f.read().strip().split('\n')


if __name__ == '__main__':

    try:
        # get site name from environment
        supported_scopes = ['select', 'premier', 'office_mgr']
        mtaf_db_host = getenv('MTAF_DB_HOST')
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description='  runs behave test on specified features directory and saves' +
                                                     '  the results on a mongodb running on a specified server\n')
        parser.add_argument("-x", "--stop", dest='stop', action='store_true')
        parser.add_argument("-d", "--db_name", type=str, default='ccd2_results', help="name of db")
        parser.add_argument("-c", "--test_class", type=str, default='regression',
                            help="class of test, e.g. regression, smoke etc.")
        parser.add_argument("-f", "--features_directory", type=str, default='eConsole/features',
                            help="operation to perform")
        parser.add_argument("-F", "--features_file", type=str, default=None,
                            help="operation to perform")
        parser.add_argument("-j", "--json_file", type=str, help="JSON file to load instead of running features")
        parser.add_argument("-s", "--server", type=str, default=mtaf_db_host,
                            help="(optional) specify mongodb server, default vqda1")
        parser.add_argument("-r", "--run_tags", type=str, default='', help="run tags (comma separated list)")
        parser.add_argument("-p", "--portal_server", type=str, default='staging',
                            choices=['staging', 'production'], help="portal server (default staging)")
        parser.add_argument("-u", "--user_scope", type=str, default=supported_scopes[0],
                            choices=supported_scopes, help="User scope (default %s)" % supported_scopes[0])
        args = parser.parse_args()
        taglist = args.run_tags.split(',')
        for tag in taglist:
            if tag in supported_scopes:
                raise Ux("supported user scope (any of %s) not allowed as run tag" % ', '.join(supported_scopes))
        fake_tag = 'fake' in taglist
        fake_detector = FakeDetector(path.join(args.features_directory, "steps"),
                                     fake_tag=fake_tag)
        args.run_tags = ','.join(taglist)
        if args.json_file:
            with open(args.json_file) as fp:
                features = json.load(fp)
        else:
            if args.features_file:
                features_dir = path.join(args.features_directory, args.features_file)
            else:
                features_dir = args.features_directory
            run_configuration = {
                'features_dir': features_dir,
                'run_tags': args.run_tags,
                'user_scope': args.user_scope,
                'portal_server': args.portal_server,
                'stop': args.stop
            }
            features = run_features(run_configuration)
        with open('app_version.txt') as f:
            app_version = f.read()
        report_configuration = {
            'installed_app': app_version,
            'site_tag': getenv('MTAF_SITE'),
            'run_tags': "%s,%s" % (args.user_scope, args.run_tags),
            'scope': args.user_scope,
            'supported_scopes': supported_scopes,
            'portal_server': args.portal_server
        }
        write_result_to_db(args, report_configuration, fake_detector, features)
        prune_db('ccd2_results', args.server, 'prune', 10, 30)
    except Ux as e:
        six.print_("User Exception: " + e.get_msg())
