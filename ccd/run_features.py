from pymongo import MongoClient
import re
import sys
import json
from behave.__main__ import main
import contextlib
import time

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


def run_features(features_dir, ccd_server):
    sys.argv = [re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])]
    sys.argv.append('-D')
    sys.argv.append('ccd_server=%s' % ccd_server)
    # sys.argv.append('-D')
    # sys.argv.append('mock')
    sys.argv.append('-f')
    sys.argv.append('json.pretty')
    sys.argv.append(features_dir)
    with capture() as out:
        main()
    # with open('output.json', 'w') as f:
    #     f.write('\n'.join(out[0].split('\n')[:-5]))
    return json.loads('\n'.join(out[0][:out[0].rindex(']') + 1].split('\n')))


def write_result_to_db(server, db_name, test_class, ccd_server, features):
    print "writing to db_name %s, server %s:" % (db_name, server)
    client = MongoClient(server)
    db = client[db_name]
    tm = time.localtime()
    start_time = time.strftime("%X", tm)
    start_date = time.strftime("%x", tm)
    fail_count = 0
    pass_count = 0
    if ccd_server == "test":
        environment = "svlab"
    else:
        environment = "production"
    for result in features:
        if result["status"] == "passed":
            pass_count += 1
        elif result["status"] == "failed":
            fail_count += 1
    test_start = {
        "app": "CCD",
        "build": "",
        "configuration": ccd_server,
        "environment": environment,
        "fail_count": fail_count,
        "pass_count": pass_count,
        "status": features[0]["status"],
        "test_class": test_class,
        "time": start_time,
        "date": start_date,
        "version": "1.x"
    }
    start_id = db["test_starts"].insert_one(test_start).inserted_id
    for feature in features:
        feature["start_id"] = start_id
        feature["test_class"] = test_class
        feature['time'] = start_time
        feature['date'] = start_date
        feature['scenarios'] = feature['elements']
        del feature['elements']
        feature['text'] = feature['name']
        del feature['name']
        for scenario in feature['scenarios']:
            scenario['text'] = scenario['name']
            scenario['status'] = 'passed'
            del scenario['name']
            if "tags" not in scenario.keys():
                scenario["tags"] = []
            for step in scenario["steps"]:
                step['text'] = step['name']
                del step['name']
                if "result" in step:
                    step["status"] = step["result"]["status"]
                    step["duration"] = step["result"]["duration"]
                    if "error_message" in step["result"]:
                        step["error_message"] = step["result"]["error_message"]
                    del step["result"]
                    if step["status"] == "failed":
                        scenario["status"] = "failed"
                else:
                    step["status"] = "passed"
                    step["duration"] = ""
        db["features"].insert_one(feature)
        # del feature['_id']
        # print json.dumps(feature, sort_keys=True, indent=4, separators=(',', ':'))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='  runs behave test on specified features directory and saves' +
                                                 '  the results on a mongodb running on a specified server\n')
    parser.add_argument("-d", "--db_name", type=str, default='ccd1_results', help="name of db")
    parser.add_argument("-c", "--test_class", type=str, default='regression',
                        help="class of test, e.g. regression, smoke etc.")
    parser.add_argument("-t", "--ccd_server", type=str, default='test', help="ccd server tag")
    parser.add_argument("-f", "--features_directory", type=str, default='ccd/reseller_features',
                        help="operation to perform")
    parser.add_argument("-s", "--server", type=str, default='localhost',
                        help="(optional) specify mongodb server, default 'localhost'")
    args = parser.parse_args()
    features = run_features(args.features_directory, args.ccd_server)
    write_result_to_db(args.server, args.db_name, args.test_class, args.ccd_server, features)


