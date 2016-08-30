#!/usr/bin/python
from pymongo import MongoClient
import re
import pprint
import json
import os
import sys

pp = pprint.PrettyPrinter(indent=4)

uri_re = re.compile('sip:([^@]+)@(.*)')


def dump_db(_db_names, cfg_dir, output_fd):
    for _db_name in db_names:
        db = client[_db_name]
        collection_names = db.collection_names()
        if 'system.indexes' in collection_names:
            collection_names.remove('system.indexes')
        all_collections = {}
        all_passwords = {}
        for collection_name in collection_names:
            print "getting collection from db: %s.%s" % (_db_name, collection_name)
            all_collections[collection_name] = []
            all_passwords[collection_name] = {}
            collection = db[collection_name]
            for c in collection.find():
                c.pop("_id", None)
                if _db_name == "test_accounts" and c['type'] == 'account':
                    all_passwords[collection_name][c["uri"]] = c.pop("password", None)
                all_collections[collection_name].append(c)
        if output_fd:
            output_fd.write(json.dumps(all_collections, sort_keys=True, indent=4, separators=(',', ': ')))
            output_fd.write('\n')
            if _db_name == "test_accounts":
                output_fd.write(json.dumps(all_passwords, sort_keys=True, indent=4, separators=(',', ': ')))
                output_fd.write('\n')
        else:
            with open(os.path.join(cfg_dir, '%s.json' % _db_name), 'w') as f:
                f.write(json.dumps(all_collections, sort_keys=True, indent=4, separators=(',', ': ')))
            if _db_name == "test_accounts":
                with open(os.path.join(cfg_dir, 'passwords.json'), 'w') as f:
                    f.write(json.dumps(all_passwords, sort_keys=True, indent=4, separators=(',', ': ')))


def restore_db(_db_names, cfg_dir, output_fd):
    all_output = {}
    for _db_name in _db_names:
        db = client[_db_name]
        with open(os.path.join(cfg_dir, '%s.json' % _db_name)) as infile:
            json_txt = infile.read()
        db_collections = json.loads(json_txt)
        all_output[_db_name] = db_collections
        all_passwords = None
        if _db_name == "test_accounts":
            with open(os.path.join(cfg_dir, 'passwords.json')) as infile:
                json_txt = infile.read()
            all_passwords = json.loads(json_txt)
        for collection_name in db_collections.keys():
            print "restoring collection: " + collection_name
            if not output_fd:
                db.drop_collection(collection_name)
            collection = db_collections[collection_name]
            if _db_name == "test_accounts":
                passwords = all_passwords[collection_name]
                for obj in collection:
                    if obj["type"] == "account":
                        obj["password"] = passwords[obj["uri"]]
            if not output_fd:
                for doc in collection:
                    db[collection_name].insert_one(doc)
    if output_fd:
        output_fd.write(json.dumps(all_output, sort_keys=True, indent=4, separators=(',', ': ')))
        output_fd.write('\n')

if __name__ == '__main__':
    import argparse
    ops = {'dump': dump_db, 'restore': restore_db}
    db_names = ['test_accounts', 'ccd_locators']
    db_args = db_names + ['all']
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='  saves and restores databases from mongodb running on SERVER\n' +
                                                 '  using JSON files in config directory for database backup;\n'
                                                 '  "dump" gets <db_name> and saves in config/<db_name>.json\n' +
                                                 '  "restore" replaces <db_name> with data from config/<db_name>.json')
    parser.add_argument("-s", "--server", type=str, default='vqda',
                        help="(optional) specify mongodb server, default 'vqda'")
    parser.add_argument("-c", "--cfg_dir", type=str, default='config/mongo_json',
                        help="(optional) specify output directory, default 'config/mongo_json'")
    parser.add_argument("-o", "--output_file", default=None,
                        help="dump writes JSON to output file, restore writes JSON to output file,\n" +
                             "db and JSON files not changed; '-' for stdout")
    parser.add_argument("operation", type=str, choices=['dump', 'restore'], help="operation to perform")
    parser.add_argument("db_name", type=str, choices=db_args, help="name of database to dump or restore")
    args = parser.parse_args()
    client = MongoClient(args.server)
    if args.output_file is None:
        output_fd = None
    elif args.output_file == '-' or args.output_file == 'stdout':
        output_fd = sys.stdout
    else:
        output_fd = open(os.path.join(args.cfg_dir, args.output_file), 'w')
    if args.db_name == 'all':
        ops[args.operation](db_names, args.cfg_dir, output_fd)
    else:
        ops[args.operation]([args.db_name], args.cfg_dir, output_fd)
    if output_fd is not None and output_fd != sys.stdout:
        output_fd.close()
