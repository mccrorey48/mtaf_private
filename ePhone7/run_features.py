from pymongo import MongoClient
import re
import sys
import json
from behave.__main__ import main
import contextlib
from datetime import datetime, timedelta
from lib.mock_steps import MockDetector
import lib.logging_esi as logging
from ePhone7.utils.configure import cfg
from lib.user_exception import UserException as Ux
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


def run_features(features_dir, site_tag, run_tags, current_aosp, downgrade_aosp, current_app, downgrade_app, ota_server,
                 stop=False):
    sys.argv = [re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])]
    sys.argv.append('-D')
    sys.argv.append('current_aosp=%s' % current_aosp)
    sys.argv.append('-D')
    sys.argv.append('downgrade_aosp=%s' % downgrade_aosp)
    sys.argv.append('-D')
    sys.argv.append('current_app=%s' % current_app)
    sys.argv.append('-D')
    sys.argv.append('downgrade_app=%s' % downgrade_app)
    sys.argv.append('-D')
    sys.argv.append('ota_server=%s' % ota_server)
    sys.argv.append('-D')
    sys.argv.append('site_tag=%s' % site_tag)
    if run_tags:
        sys.argv.append('--tags=%s' % run_tags)
    if stop:
        sys.argv.append('--stop')
    sys.argv.append('-f')
    sys.argv.append('json.pretty')
    sys.argv.append(features_dir)
    start_time = datetime.now()
    with capture() as out:
        main()
    json_repr = '\n'.join(out[0][:out[0].rindex(']') + 1].split('\n'))
    with open('output_pre.json', 'w') as f:
        f.write(json_repr)
    data = json.loads(json_repr)
    if len(data):
        data[0]["start_time"] = start_time.strftime("%X")
        data[0]["start_date"] = start_time.strftime("%x")
    json_repr = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    with open('output.json', 'w') as f:
        f.write(json_repr)
    return data


def write_result_to_db(server, db_name, test_class, environment, configuration, mock_detector, features):
    print 'writing to db_name %s, server %s:' % (db_name, server)
    client = MongoClient(server)
    db = client[db_name]
    step_re = re.compile('\s*(\[\s*([^]]*\S)\s*\]\s*)?\s*(.*\S)\s*')
    if len(features) and 'start_time' in features[0] and 'start_date' in features[0]:
        start_datetime = datetime.strptime("%s %s" % (features[0]['start_date'], features[0]['start_time']), '%x %X')
    else:
        start_datetime = datetime.now()
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
        'time': start_datetime.strftime('%X'),
        'date': start_datetime.strftime('%x'),
        'version': '1.x'
    }
    start_id = db['test_starts'].insert_one(test_start).inserted_id
    fail_count = 0
    pass_count = 0
    skip_count = 0
    start_result = 'passed'
    for iter_num, feature in enumerate(features):
        feature_has_skips = False
        feature_has_fakes = False
        feature_has_fails = False
        feature_has_passes = False
        feature_has_incompletes = False
        feature['start_id'] = start_id
        feature['test_class'] = test_class
        feature['text'] = feature['name']
        del feature['name']
        feature['time'] = start_datetime.strftime('%X')
        feature['date'] = start_datetime.strftime('%x')
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
            scenario['time'] = start_datetime.strftime('%X')
            scenario['date'] = start_datetime.strftime('%x')
            for step in scenario['steps']:
                m = step_re.match(step['name'])
                if m:
                    step['text'] = m.group(3)
                else:
                    step['text'] = step['name']
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
                            if step['name'] in background_steps:
                                step['status'] = 'fake bg'
                            else:
                                step['status'] = 'fake'
                            step['duration'] = 0.1
                            scenario_has_fakes = True
                        elif step['name'] in background_steps:
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
                    start_datetime += timedelta(seconds=step['duration'])
                else:
                    step['status'] = 'skipped'
                    scenario_has_skips = True
                    step['duration'] = 0.0
                del step['name']
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
    from os import path, getenv, listdir, mkdir
    import spur
    import shutil

    try:
        # get site name from environment
        mtaf_site = getenv('MTAF_SITE')
        if not mtaf_site:
            raise Ux('MTAF_SITE must be defined in the run-time environment')
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
        parser.add_argument("-t", "--site_tag", type=str, default=mtaf_site, help="site tag (default %s)" % mtaf_site)
        parser.add_argument("-o", "--downgrade_aosp", type=str, default='2.1.3', help="apk version (default 2.1.3)")
        parser.add_argument("-O", "--ota_server", type=str, default='alpha', help="OTA server (default alpha")
        parser.add_argument("-a", "--downgrade_app", type=str, default='1.0.10', help="apk version (default 1.0.10)")
        args = parser.parse_args()
        cfg.set_site(args.server, args.site_tag)
        build_prop_server = cfg.site["BuildPropServer"]
        build_image_server = cfg.site["BuildImageServer"]
        aosps_home = cfg.site["AospsHome"]
        apks_home = cfg.site["ApksHome"]
        mock_detector = MockDetector(path.join(args.features_directory, "steps"),
                                fake_tag='fake' in args.run_tags.split(','))

        # make sure both aosps_home and apks_home directories exist
        try:
            mkdir(aosps_home)
        except OSError:
            pass
        try:
            mkdir(apks_home)
        except OSError:
            pass

        # get the current version from the build server
        shell = spur.SshShell(
            hostname=build_prop_server,
            username='ubuntu',
            private_key_file='ePhone7/keys/OTAServer2.pem',
            missing_host_key=spur.ssh.MissingHostKey.accept
        )
        with shell:
            if args.ota_server == 'alpha':
                result = shell.run(['cat', '/www/aus/otatest/build.prop'])
            else:
                result = shell.run(['cat', '/www/aus/beta/otatest/build.prop'])
        current_aosp = None
        current_app = None
        aosp_prefix = 'ro.build.id='
        aosp_new_prefix = 'system.version='
        app_prefix = 'app.version='
        for line in result.output.split('\n'):
            line = line.strip()
            if line.startswith(aosp_prefix):
                current_aosp = line[len(aosp_prefix):]
            elif line.startswith(aosp_new_prefix):
                current_aosp = line[len(aosp_new_prefix):]
            elif line.startswith(app_prefix):
                current_app = line[len(app_prefix):]
        if current_aosp is None:
            raise Ux("current_aosp not found")
        elif current_app is None:
            raise Ux("current_app not found")

        # make sure the downgrade versions of the aosp and apk are available
        aosp_dirs = listdir(aosps_home)
        apks = listdir(apks_home)
        if not args.downgrade_aosp in aosp_dirs:
            mkdir(path.join(aosps_home, args.downgrade_aosp))
        shell = spur.SshShell(
            hostname=build_image_server,
            username='root',
            password='root',
            missing_host_key=spur.ssh.MissingHostKey.accept
        )
        aosp_downgrade_images = listdir(path.join(aosps_home, args.downgrade_aosp))
        with shell:
            for basename in ['boot', 'system', 'recovery']:
                img_filename = basename + '.img'
                remote_img_path = 'aosps/%s/%s' % ('_'.join(['build'] + args.downgrade_aosp.split('.')), img_filename)
                print "remote file: " + remote_img_path
                local_img_path = path.join(aosps_home, args.downgrade_aosp, img_filename)
                print "local file: " + local_img_path + '...',
                if img_filename in aosp_downgrade_images:
                    print "already downloaded to test host"
                else:
                    print "downloading to test host"
                    with shell.open(remote_img_path, 'rb') as remote_file:
                        with open(local_img_path, 'wb') as local_file:
                            shutil.copyfileobj(remote_file, local_file)
            remote_apk_filename = 'update.apk.%02d%02d%02d' % tuple([int(n) for n in args.downgrade_app.split('.')])
            local_apk_filename = args.downgrade_app + '.apk'
            remote_apk_path = 'apks/' + remote_apk_filename
            local_apk_path = path.join(apks_home, local_apk_filename)
            print "remote file: " + remote_apk_path
            print "local file: " + remote_apk_path + '...',
            if local_apk_filename in apks:
                print "already downloaded to test host"
            else:
                print "downloading to test host"
                with shell.open(remote_apk_path, 'rb') as remote_file:
                    with open(local_apk_path, 'wb') as local_file:
                        shutil.copyfileobj(remote_file, local_file)

        if args.json_file:
            with open(args.json_file) as fp:
                features = json.load(fp)
        else:
            features = run_features(args.features_directory, args.site_tag, args.run_tags, current_aosp,
                                    args.downgrade_aosp, current_app, args.downgrade_app, args.ota_server)
        configuration = "site_tag:%s, run_tags:%s" % (args.site_tag, args.run_tags)
        write_result_to_db(args.server, args.db_name, args.test_class, args.environment, configuration, mock_detector, features)
    except Ux as e:
        print "User Exception: " + e.get_msg()

