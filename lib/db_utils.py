from pymongo import MongoClient
import re
import pprint
import json
import os
import sys

pp = pprint.PrettyPrinter(indent=4)

uri_re = re.compile('sip:([^@]+)@(.*)')


def read_dbs(_db_names, server):
    client = MongoClient(server)
    all_dbs = {}
    for _db_name in _db_names:
        db = client[_db_name]
        collection_names = db.collection_names()
        if 'system.indexes' in collection_names:
            collection_names.remove('system.indexes')
        all_dbs[_db_name] = {}
        for collection_name in collection_names:
            print "getting collection from db: %s.%s" % (_db_name, collection_name)
            all_dbs[_db_name][collection_name] = []
            for doc in db[collection_name].find():
                all_dbs[_db_name][collection_name].append(doc)
    return all_dbs


def dump_dbs(_db_names, server, cfg_dir, _output_fd):
    all_dbs = read_dbs(_db_names, server)
    for _db_name in _db_names:
        use_passwords_file = False
        db_dict = all_dbs[_db_name]
        if _db_name.endswith("_site"):
            passwords = {}
        for collection_name in db_dict:
            if _db_name.endswith("_site"):
                passwords[collection_name] = {}
            for doc in db_dict[collection_name]:
                doc.pop("_id")
                if _db_name.endswith("_site") and doc['type'] == 'account':
                    if 'password' in doc:
                        passwords[collection_name][doc['uri']] = doc.pop('password', None)
                        use_passwords_file = True
        if _output_fd:
            _output_fd.write("%s\n" % _db_name)
            _output_fd.write(json.dumps(db_dict, sort_keys=True, indent=4, separators=(',', ': ')))
            _output_fd.write('\n')
        else:
            with open(os.path.join(cfg_dir, '%s.json' % _db_name), 'w') as f:
                f.write(json.dumps(db_dict, sort_keys=True, indent=4, separators=(',', ': ')))
        if use_passwords_file:
            if _output_fd:
                _output_fd.write("passwords\n")
                _output_fd.write(json.dumps(passwords, sort_keys=True, indent=4, separators=(',', ': ')))
                _output_fd.write('\n')
            else:
                with open(os.path.join(cfg_dir, 'passwords.json'), 'w') as f:
                    f.write(json.dumps(passwords, sort_keys=True, indent=4, separators=(',', ': ')))


def restore_dbs(_db_names, server, cfg_dir, _output_fd):
    all_output = {}
    all_collections = {}
    for _db_name in _db_names:
        with open(os.path.join(cfg_dir, '%s.json' % _db_name)) as infile:
            json_txt = infile.read()
        db_collections = json.loads(json_txt)
        all_output[_db_name] = db_collections
        if _db_name.endswith("_site"):
            try:
                with open(os.path.join(cfg_dir, 'passwords.json')) as infile:
                    all_passwords = json.loads(infile.read())
            except IOError:
                all_passwords = {}
        for collection_name in db_collections.keys():
            print "restoring collection: " + collection_name
            collection = db_collections[collection_name]
            if _db_name.endswith("_site") and collection_name in all_passwords:
                passwords = all_passwords[collection_name]
                for doc in collection:
                    try:
                        if doc['type'] == 'account' and doc['uri'] in passwords:
                            doc['password'] = passwords[doc['uri']]
                    except KeyError:
                        pass
        all_collections[_db_name] = db_collections
    if not _output_fd:
        write_dbs(all_collections, server)
    if _output_fd:
        _output_fd.write(json.dumps(all_output, sort_keys=True, indent=4, separators=(',', ': ')))
        _output_fd.write('\n')


def write_dbs(all_collections, server):
    client = MongoClient(server)
    for _db_name in all_collections.keys():
        db = client[_db_name]
        for collection_name in all_collections[_db_name].keys():
            collection = all_collections[_db_name][collection_name]
            db.drop_collection(collection_name)
            for doc in collection:
                db[collection_name].insert_one(doc)


if __name__ == '__main__':
    import argparse
    ops = {'dump': dump_dbs, 'restore': restore_dbs}
    dbs = ['e7_site', 'ccd_site']
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='  saves and restores databases from mongodb running on SERVER\n' +
                                                 '  using JSON files in config directory for database backup;\n'
                                                 '  "dump" gets <db_name> and saves in config/<db_name>.json\n' +
                                                 '  "restore" replaces <db_name> with data from config/<db_name>.json')
    parser.add_argument("-s", "--server", type=str, default='vqda',
                        help="(optional) specify mongodb server, default 'vqda'")
    parser.add_argument("-c", "--cfg_dir", type=str, default='config',
                        help="(optional) specify output directory, default 'config'")
    parser.add_argument("-o", "--output_file", default=None,
                        help="dump writes JSON to output file, restore writes JSON to output file,\n" +
                             "db and JSON files not changed; '-' for stdout")
    parser.add_argument("operation", type=str, choices=['dump', 'restore'], help="operation to perform")
    parser.add_argument("db_name", type=str, choices=dbs, help="name of database to dump or restore")
    args = parser.parse_args()
    if args.output_file is None:
        ops[args.operation]([args.db_name], args.server, args.cfg_dir, None)
    elif args.output_file == '-' or args.output_file == 'stdout':
        ops[args.operation]([args.db_name], args.server, args.cfg_dir, sys.stdout)
    else:
        with open(os.path.join(args.cfg_dir, args.output_file), 'w') as output_fd:
            ops[args.operation]([args.db_name], args.server, args.cfg_dir, output_fd)
