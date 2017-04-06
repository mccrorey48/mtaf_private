from pymongo import MongoClient
import re
import sys
import json
from behave.__main__ import main
import contextlib
from datetime import datetime, timedelta
from lib.mock_steps import MockDetector
import lib.logging_esi as logging
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


def run_features(features_dir, site_tag, run_tags, version):
    sys.argv = [re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])]
    sys.argv.append('-D')
    sys.argv.append('version=%s' % version)
    sys.argv.append('-D')
    sys.argv.append('site_tag=%s' % site_tag)
    if run_tags:
        sys.argv.append('--tags=%s' % run_tags)
    sys.argv.append('--stop')
    sys.argv.append('-f')
    sys.argv.append('json.pretty')
    sys.argv.append(features_dir)
    with capture() as out:
        main()
    with open('output.json', 'w') as f:
        f.write('\n'.join(out[0][:out[0].rindex(']') + 1].split('\n')))
    return json.loads('\n'.join(out[0][:out[0].rindex(']') + 1].split('\n')))


def write_result_to_db(server, db_name, test_class, environment, configuration, mock_detector, features):
    print 'writing to db_name %s, server %s:' % (db_name, server)
    client = MongoClient(server)
    db = client[db_name]
    start_time = datetime.now()
    test_start = {
        'app': 'ePhone7',
        'build': '',
        'configuration': configuration,
        'environment': environment,
        'fail_count': 0,
        'skip_count': 0,
        'pass_count': 0,
        'status': '',
        'test_class': test_class,
        'time': start_time.strftime('%X'),
        'date': start_time.strftime('%x'),
        'version': '1.x'
    }
    start_id = db['test_starts'].insert_one(test_start).inserted_id
    fail_count = 0
    pass_count = 0
    skip_count = 0
    start_result = 'passed'
    for feature in features:
        feature_has_skips = False
        feature_has_fakes = False
        feature_has_fails = False
        feature_has_passes = False
        feature_has_incompletes = False
        feature['start_id'] = start_id
        feature['test_class'] = test_class
        feature['text'] = feature['name']
        del feature['name']
        feature['time'] = start_time.strftime('%X')
        feature['date'] = start_time.strftime('%x')
        background_steps = []
        feature['scenarios'] = []
        feature['duration'] = 0.0
        for element in feature['elements']:
            if element['keyword'] == 'Background':
                background_steps = [step['name'] for step in element['steps']]
            else:
                feature['scenarios'].append(element)
        for scenario in feature['scenarios']:
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
            scenario['time'] = start_time.strftime('%X')
            scenario['date'] = start_time.strftime('%x')
            for step in scenario['steps']:
                step['text'] = step['name']
                del step['name']
                if 'result' in step:
                    # once a step in a scenario fails, the rest of the steps will be skipped
                    # so step won't have a 'result' attribute and they will be assigne "skipped"
                    # status in the "else" branch of this "if" statement
                    step['status'] = step['result']['status']
                    step['duration'] = step['result']['duration']
                    if step['status'] == 'failed':
                        scenario_has_fails = True
                    elif step['status'] == 'passed':
                        # "passed" steps can be fake or background, fake gets priority if both apply
                        if mock_detector.match(step['text']):
                            step['status'] = 'fake'
                            step['duration'] = 0.1
                            scenario_has_fakes = True
                        elif step['text'] in background_steps:
                            step['status'] = 'background'
                        else:
                            scenario_has_passes = True
                    if 'error_message' in step['result']:
                        step['error_message'] = step['result']['error_message']
                    else:
                        step['error_message'] = ''
                    del step['result']
                    scenario['duration'] += step['duration']
                    feature['duration'] += step['duration']
                    start_time += timedelta(seconds=step['duration'])
                else:
                    step['status'] = 'skipped'
                    scenario_has_skips = True
                    step['duration'] = 0.0
            #
            # scenario_has status table
            # ------------------------------------------------------------------------
            #   fakes   |    skips     |      fails     |    passes    ||   status
            # ------------------------------------------------------------------------
            #   False   |    False     |      False     |    False     ||   undefined
            #   False   |    False     |      False     |    True      ||   passed
            #   False   |    False     |      True      |    False     ||   failed
            #   False   |    False     |      True      |    True      ||   failed
            #   False   |    True      |      False     |    False     ||   skipped
            #   False   |    True      |      False     |    True      ||   incomplete
            #   False   |    True      |      True      |    False     ||   failed
            #   False   |    True      |      True      |    True      ||   failed
            #   True    |    False     |      False     |    False     ||   fake
            #   True    |    False     |      False     |    True      ||   fake
            #   True    |    False     |      True      |    False     ||   fake
            #   True    |    False     |      True      |    True      ||   fake
            #   True    |    True      |      False     |    False     ||   fake
            #   True    |    True      |      False     |    True      ||   fake
            #   True    |    True      |      True      |    False     ||   fake
            #   True    |    True      |      True      |    True      ||   fake
            #
            if scenario_has_fakes:
                scenario['status'] = 'fake'
                feature_has_fakes = True
            elif scenario_has_fails:
                scenario['status'] = 'failed'
                feature_has_fails = True
            elif scenario_has_skips:
                if scenario_has_passes:
                    scenario['status'] = 'incomplete'
                    feature_has_incompletes = True
                else:
                    scenario['status'] = 'skipped'
                    feature_has_skips = True
            elif scenario_has_passes:
                scenario['status'] = 'passed'
                feature_has_passes = True
            else:
                scenario['status'] = 'undefined'
        del feature['elements']
        if feature_has_fakes:
            feature['status'] = 'fake'
        elif feature_has_fails:
            if feature_has_skips:
                feature['status'] = 'incomplete'
            else:
                feature['status'] = 'failed'
        elif feature_has_incompletes:
            feature['status'] = 'incomplete'
        elif feature_has_passes:
            if feature_has_skips:
                feature['status'] = 'incomplete'
            else:
                feature['status'] = 'passed'
        elif feature_has_skips:
            feature['status'] = 'skipped'
        else:
            feature['status'] = 'undefined'
        db['features'].insert_one(feature)
        # del feature['start_id']
        # print json.dumps(feature, sort_keys=True, indent=4, separators=(',', ':'))
    for feature in features:
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
    import argparse
    from os import path
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='  runs behave test on specified features directory and saves' +
                                                 '  the results on a mongodb running on a specified server\n')
    parser.add_argument("-d", "--db_name", type=str, default='e7_results', help="name of db")
    parser.add_argument("-c", "--test_class", type=str, default='regression',
                        help="class of test, e.g. regression, smoke etc.")
    parser.add_argument("-e", "--environment", type=str, default='production', help="environment e.g. production")
    parser.add_argument("-f", "--features_directory", type=str, default='ePhone7/features',
                        help="operation to perform")
    parser.add_argument("-j", "--json_file", type=str, help="JSON file to load instead of running features")
    parser.add_argument("-s", "--server", type=str, default='vqda1',
                        help="(optional) specify mongodb server, default vqda1")
    parser.add_argument("-r", "--run_tags", type=str, default='wip', help="run tags (comma separated list)")
    parser.add_argument("-t", "--site_tag", type=str, default='mm', help="site tag (default mm)")
    parser.add_argument("-v", "--version", type=str, default='1.2.0', help="apk version (default 1.2.0)")
    args = parser.parse_args()
    mock_detector = MockDetector(path.join(args.features_directory, "steps", "steps.py"),
                            fake_tag='fake' in args.run_tags.split(','))
    if args.json_file:
        with open(args.json_file) as fp:
            features = json.load(fp)
    else:
        features = run_features(args.features_directory, args.site_tag, args.run_tags, args.version)
    configuration = "site_tag:%s, run_tags:%s" % (args.site_tag, args.run_tags)
    write_result_to_db(args.server, args.db_name, args.test_class, args.environment, configuration, mock_detector, features)



