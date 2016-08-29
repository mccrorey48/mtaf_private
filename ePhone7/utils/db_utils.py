#!/usr/bin/python
from pymongo import MongoClient
import re
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)

uri_re = re.compile('sip:([^@]+)@(.*)')


def dump_db(_db_name, use_stdout=False):
    db = client[_db_name]
    collection_names = db.collection_names()
    if 'system.indexes' in collection_names:
        collection_names.remove('system.indexes')
    if 'users' in collection_names:
        collection_names.remove('users')
    if 'customers' in collection_names:
        collection_names.remove('customers')
    all_collections = {}
    for collection_name in collection_names:
        print "getting collection from db: %s.%s" % (_db_name, collection_name)
        all_collections[collection_name] = []
        collection = db[collection_name]
        for c in collection.find():
            c.pop("_id", None)
            all_collections[collection_name].append(c)
    if use_stdout:
        print json.dumps(all_collections, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        with open('config/%s.json' % _db_name, 'w') as f:
            f.write(json.dumps(all_collections, sort_keys=True, indent=4, separators=(',', ': ')))



def restore_db(_db_name, use_stdout):
    db = client[_db_name]
    with open('config/%s.json' % _db_name) as infile:
        json_txt = infile.read()
    all_collections = json.loads(json_txt)
    for collection_name in all_collections.keys():
        print "restoring collection: " + collection_name
        db.drop_collection(collection_name)
        collection = all_collections[collection_name]
        if use_stdout:
            print json.dumps(collection, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            for doc in collection:
                db[collection_name].insert_one(doc)

if __name__ == '__main__':
    import argparse
    ops = {'dump': dump_db, 'restore': restore_db}
    db_names = ['results_ePhone7', 'daily_results_ePhone7', 'results_logtest', 'results_re_test', 'results_wrappers_test']
    db_args = db_names + ['all']
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='  saves and restores databases from mongodb running on SERVER\n' +
                                                 '  using JSON files in config directory for database backup;\n'
                                                 '  "dump" gets <db_name> and saves in config/<db_name>.json\n' +
                                                 '  "restore" replaces <db_name> with data from config/<db_name>.json')
    parser.add_argument("-s", "--server", type=str, default='vqda',
                        help="(optional) specify mongodb server, default 'vqda'")
    parser.add_argument("--stdout", action='store_true',
                        help="dump prints db to stdout, restore prints JSON file content to stdout\n" +
                             "db and JSON files not changed")
    parser.add_argument("operation", type=str, choices=['dump', 'restore'], help="operation to perform")
    parser.add_argument("db_name", type=str, choices=db_args, help="name of database to dump or restore")
    args = parser.parse_args()
    client = MongoClient(args.server)
    if args.db_name == 'all':
        for db_name in db_names:
            ops[args.operation](db_name, args.stdout)
    else:
        ops[args.operation](args.db_name, args.stdout)
