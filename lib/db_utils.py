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
            del db_dict['constants']
            del db_dict['user']
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
            constants = []
            user = []
            try:
                with open(os.path.join(cfg_dir, 'passwords.json')) as infile:
                    all_passwords = json.loads(infile.read())
            except IOError:
                all_passwords = {}
            for collection_name in db_collections.keys():
                print "processing collection " + collection_name
                if collection_name in all_passwords:
                    passwords = all_passwords[collection_name]
                for doc in db_collections[collection_name]:
                    try:
                        if collection_name in all_passwords and doc['type'] == 'account' and doc['uri'] in passwords:
                            doc['password'] = passwords[doc['uri']]
                    except KeyError:
                        pass
                    try:
                        if doc['type'] == 'user':
                            user.append(dict(doc, **{'site_tag': collection_name}))
                        elif doc['type'] == 'constants':
                            constants.append(dict(doc, **{'site_tag': collection_name}))
                    except KeyError:
                        pass
            db_collections['constants'] = constants
            db_collections['user'] = user
        print "restoring db: " + _db_name
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
    targets = {
        'ego_android_site': {"cfg_dir": os.path.join('ePhoneGoAndroid', 'config'), "db_names": ['ego_android_site']},
        'ego_android_all': {"cfg_dir": os.path.join('ePhoneGoAndroid', 'config'),
                            "db_names": ['ego_android_site', 'ego_android_caps']},
        'e7_site': {"cfg_dir": os.path.join('ePhone7', 'config'), "db_names": ['e7_site']},
        'e7_all': {"cfg_dir": os.path.join('ePhone7', 'config'), "db_names": ['e7_site', 'e7_caps', 'e7_colors']},
        'ccd_site': {"cfg_dir": os.path.join('ccd', 'config'), "db_names": ['ccd_site']}
    }
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='  saves and restores databases from mongodb running on SERVER\n' +
                                                 '  using JSON files in config directory for database backup;\n' +
                                                 '  "dump" gets <db_name> and saves in ' +
                                                 '<target config directory>/<db_name>.json\n' +
                                                 '  "restore" replaces <db_name> with data from ' +
                                                 '<target config directory>/<db_name>.json')
    parser.add_argument("-s", "--server", type=str, default='vqda',
                        help="(optional) specify mongodb server, default 'vqda'")
    parser.add_argument("-o", "--output_file", default=None,
                        help="dump writes JSON to output file, restore writes JSON to output file,\n" +
                             "db and JSON files not changed; '-' for stdout")
    parser.add_argument("operation", type=str, choices=['dump', 'restore'], help="operation to perform")
    parser.add_argument("target", type=str, choices=targets.keys(),
                        help='indicates databases to dump or restore:\n' +
                             '  e7_site: db name e7_site; config directory ePhone7/config\n' +
                             '  e7_all: db names e7_site, caps, colors; config directory ePhone7/config\n' +
                             '  ccd_site: db name ccd_site; config directory ccd/config\n')
    args = parser.parse_args()
    db_names = targets[args.target]['db_names']
    cfg_dir = targets[args.target]['cfg_dir']
    if args.output_file is None:
        ops[args.operation](db_names, args.server, cfg_dir, None)
    elif args.output_file == '-' or args.output_file == 'stdout':
        ops[args.operation](db_names, args.server, cfg_dir, sys.stdout)
    else:
        with open(os.path.join(cfg_dir, args.output_file), 'w') as output_fd:
            ops[args.operation](db_names, args.server, cfg_dir, output_fd)
