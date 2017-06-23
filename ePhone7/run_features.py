import contextlib
import json
import re
import sys
from datetime import datetime, timedelta
from behave.__main__ import main
from pymongo import MongoClient
import lib.logging_esi as logging
from ePhone7.config.configure import cfg
from lib.mock_steps import MockDetector
from lib.user_exception import UserException as Ux
from lib.wrappers import Trace
import argparse
from os import path, getenv
from ePhone7.utils.versions import *
from shutil import copyfile

log = logging.get_logger('esi.run_features')


@contextlib.contextmanager
def capture():
    import sys
    from cStringIO import StringIO
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
    sys.argv = [re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])]
    sys.argv.append('-D')
    sys.argv.append('ota_server=%s' % config['ota_server'])
    if config['run_tags']:
        sys.argv.append('--tags=%s' % config['run_tags'])
    if config['stop']:
        sys.argv.append('--stop')
    sys.argv.append('-f')
    sys.argv.append('json.pretty')
    sys.argv.append(config['features_dir'])
    start_time = datetime.now()
    with capture() as out:
        main()
    with open('main.json', 'w') as f:
        f.write(out[0])
    with open('steps.txt', 'r') as f:
        not_json_prefix = f.read()
    printed_steps = []
    current_step = None
    for line in not_json_prefix.strip().split('\n'):
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
    if current_step is not None:
        printed_steps.append(current_step)
    json_repr = '\n'.join(out[0][:out[0].rindex(']') + 1].split('\n'))
    with open('json_repr.json', 'w') as f:
        f.write(json_repr)
    data = json.loads(json_repr)
    if len(data):
        data[0]["start_time"] = start_time.strftime("%X")
        data[0]["start_date"] = start_time.strftime("%x")
    for feature in data:
        for element in feature["elements"]:
            if element["keyword"] == "Scenario":
                new_steps = []
                for step in element["steps"]:
                    if "result" in step:
                        # if it gets to here, the step was executed and should be on the printed_steps list
                        if len(printed_steps) == 0:
                            raise Ux("Error processing new_steps list, printed_steps empty")
                        printed_step = printed_steps.pop(0)
                        if printed_step["name"] != step["name"]:
                            raise Ux("Error processing new_steps list, step name mismatch")
                        step["substeps"] = printed_step["substeps"]
                    new_steps.append(step)
                element["steps"] = new_steps
    json_repr = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    with open('output.json', 'w') as f:
        f.write(json_repr)
    copyfile('log/esi_info.log', 'log/esi_info_copy.log')
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


def write_result_to_db(_args, configuration, _mock_detector, _features):
    print 'writing to db_name %s, server %s:' % (_args.db_name, _args.server)
    client = MongoClient(_args.server)
    db = client[_args.db_name]
    if len(_features) and 'start_time' in _features[0] and 'start_date' in _features[0]:
        start_datetime = datetime.strptime("%s %s" % (_features[0]['start_date'], _features[0]['start_time']), '%x %X')
    else:
        start_datetime = datetime.now()
    test_start = {
        'app': 'ePhone7',
        'build': '',
        'configuration': configuration,
        'environment': _args.environment,
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
    start_result = 'passed'
    if _args.json_file:
        info_filename = 'log/esi_info_copy.log'
    else:
        info_filename = 'log/esi_info.log'
    stepinfo = StepInfo(info_filename)
    last_step_duration = 0
    for iter_num, feature in enumerate(_features):
        feature_has_skips = False
        feature_has_fakes = False
        feature_has_fails = False
        feature_has_passes = False
        feature['start_id'] = start_id
        feature['test_class'] = _args.test_class
        feature['text'] = feature['name']
        del feature['name']
        feature['order'] = iter_num
        background_steps = []
        feature['scenarios'] = []
        feature['duration'] = 0.0
        for element in feature['elements']:
            if element['keyword'] == 'Background':
                background_steps = [step['name'] for step in element['steps']]
            else:
                feature['scenarios'].append(element)
        for scenario_index, scenario in enumerate(feature['scenarios']):
            scenario_has_skips = False
            scenario_has_fakes = False
            scenario_has_fails = False
            scenario_has_passes = False
            scenario['text'] = scenario['name']
            scenario['status'] = 'passed'
            del scenario['name']
            if 'tags' not in scenario.keys():
                scenario['tags'] = []
            scenario['duration'] = 0.0
            for step_index, step in enumerate(scenario['steps']):
                step['text'] = rm_view_prefix(step['name'])
                if 'result' in step:
                    # if 'result' is not in step, the step was skipped, either because it belongs
                    # to a scenario that was skipped (because it didn't have the right tag)
                    # or a previous step in the current scenario failed
                    step['status'] = step['result']['status']
                    step['duration'] = step['result']['duration']
                    _date, _time = stepinfo.parse(feature['text'], scenario['text'], step['text']).next()
                    if "substeps" in step:
                        for substep in step["substeps"]:
                            _date, _time = stepinfo.parse(feature['text'], scenario['text'], substep['text']).next()
                            start_datetime = datetime.strptime("%s %s" % (_date, _time), '%x %X')
                            substep['time'] = start_datetime.strftime('%X')
                            substep['date'] = start_datetime.strftime('%x')
                            if substep["status"] == 'failed':
                                step['status'] = 'failed'
                            elif substep['status'] == 'passed':
                                if _mock_detector.match(substep["name"]):
                                    substep['status'] = 'fake'
                    if _mock_detector.match(step['name']):
                        step['status'] = 'fake'
                    else:
                        if step['status'] == 'failed':
                            scenario_has_fails = True
                        elif step['status'] == 'passed':
                            if step['name'] not in background_steps:
                                scenario_has_passes = True
                    if 'error_message' in step['result']:
                        step['error_message'] = step['result']['error_message']
                    else:
                        step['error_message'] = ''
                    del step['result']
                    start_datetime = datetime.strptime("%s %s" % (_date, _time), '%x %X')
                    scenario['duration'] += step['duration']
                    feature['duration'] += step['duration']
                else:
                    # steps without a 'result' attribute will be assigned "skipped" status
                    step['status'] = 'skipped'
                    scenario_has_skips = True
                    step['duration'] = 0.0
                    start_datetime += timedelta(seconds=last_step_duration)
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

            if scenario_has_fails:
                scenario['status'] = 'failed'
                feature_has_fails = True
            elif scenario_has_skips:
                scenario['status'] = 'skipped'
                feature_has_skips = True
            elif scenario_has_fakes:
                scenario['status'] = 'fake'
                feature_has_fakes = True
            elif scenario_has_passes:
                scenario['status'] = 'passed'
                feature_has_passes = True
            else:
                # no steps
                scenario['status'] = 'fake'
                feature_has_fakes = True

        del feature['elements']
        if feature_has_fails:
            feature['status'] = 'failed'
        elif feature_has_fakes:
            feature['status'] = 'fake'
        elif feature_has_skips:
            if feature_has_passes:
                feature['status'] = 'incomplete'
            else:
                feature['status'] = 'skipped'
        elif feature_has_passes:
            feature['status'] = 'passed'
        else:
            feature['status'] = 'undefined'
        db['features'].insert_one(feature)
        # del feature['start_id']
        # print json.dumps(feature, sort_keys=True, indent=4, separators=(',', ':'))
    for feature in _features:
        if feature['status'] == 'passed':
            pass_count += 1
        elif feature['status'] == 'skipped':
            skip_count += 1
        elif feature['status'] == 'failed':
            fail_count += 1
            start_result = 'failed'
    db['test_starts'].find_one_and_update({"_id": start_id}, {'$set': {'pass_count': pass_count,
                                                                       'fail_count': fail_count,
                                                                       'skip_count': skip_count,
                                                                       'status': start_result}})
if __name__ == '__main__':

    try:
        # get site name from environment
        mtaf_db_host = getenv('MTAF_DB_HOST')
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description='  runs behave test on specified features directory and saves' +
                                                     '  the results on a mongodb running on a specified server\n')
        parser.add_argument("-x", "--stop", dest='stop', action='store_true')
        parser.add_argument("-d", "--db_name", type=str, default='e7_results', help="name of db")
        parser.add_argument("-c", "--test_class", type=str, default='regression',
                            help="class of test, e.g. regression, smoke etc.")
        parser.add_argument("-e", "--environment", type=str, default='production', help="environment e.g. production")
        parser.add_argument("-f", "--features_directory", type=str, default='ePhone7/features',
                            help="operation to perform")
        parser.add_argument("-F", "--features_file", type=str, default=None,
                            help="operation to perform")
        parser.add_argument("-j", "--json_file", type=str, help="JSON file to load instead of running features")
        parser.add_argument("-s", "--server", type=str, default=mtaf_db_host,
                            help="(optional) specify mongodb server, default vqda1")
        parser.add_argument("-r", "--run_tags", type=str, default='', help="run tags (comma separated list)")
        parser.add_argument("-o", "--downgrade_aosp", type=str, default='2.3.7',
                            help="aosp downgrade version (default 2.3.7)")
        parser.add_argument("-O", "--ota_server", type=str, default='alpha',
                            choices=['alpha', 'beta', 'prod'], help="OTA server (default alpha")
        parser.add_argument("-a", "--downgrade_app", type=str, default='1.3.6',
                            help="apk downgrade version (default 1.3.6)")
        args = parser.parse_args()
        fake_tag = 'fake' in args.run_tags.split(',')
        mock_detector = MockDetector(path.join(args.features_directory, "steps"),
                                     fake_tag=fake_tag)
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
                'ota_server': args.ota_server,
                'stop': args.stop
            }
            features = run_features(run_configuration)
        if fake_tag or args.json_file:
            installed_aosp, installed_app = 'fake', 'fake'
        else:
            installed_aosp, installed_app = get_current_versions(args.ota_server)
        report_configuration = "site_tag:%s, run_tags:%s, installed_aosp:%s, installed_app:%s" % \
                               (cfg.site_tag, args.run_tags, installed_aosp, installed_app)
        write_result_to_db(args, report_configuration, mock_detector, features)
    except Ux as e:
        print "User Exception: " + e.get_msg()
