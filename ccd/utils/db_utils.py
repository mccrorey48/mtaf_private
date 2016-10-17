from pymongo import MongoClient
import re
import pprint
import json
import os
import sys
from lib.user_exception import UserException as Ux

pp = pprint.PrettyPrinter(indent=4)

uri_re = re.compile('sip:([^@]+)@(.*)')


class CfgReader:
    account_configs = {}
    locators = {}
    platform_configs = {}
    domain_configs = {}
    pbfile_strings = {}
    platform_names = ['production', 'svlab']

    def __init__(self, mongo_server='vqda'):
        self.client = MongoClient(mongo_server)

    def get_account_configs(self):
        return self.account_configs

    def get_pbfile_strings(self):
        return self.pbfile_strings

    def get_locators(self):
        return self.locators

    def get_platform_configs(self):
        return self.platform_configs

    def get_domain_configs(self):
        return self.domain_configs

    def get_ini_tags(self, platform_name):
        db = self.client.ccd_accounts
        if platform_name in self.platform_names:
            return db[platform_name].find_one({"type": "ini_tags"})['values']


    @staticmethod
    def stringify(thing):
        # convert unicode to str because pjsip doesn't like unicode
        if type(thing) is unicode:
            return str(thing)
        elif type(thing) is dict:
            newdict = {}
            for key in thing:
                newdict[str(key)] = CfgReader.stringify(thing[key])
            return newdict
        elif type(thing) is list:
            return [CfgReader.stringify(item) for item in thing]

    def read_account_cfg_from_db(self, server_tag, context, use_dtmf_audio=True):
        db = self.client.ccd_accounts
        for platform_name in self.platform_names:
            if server_tag in db[platform_name].find_one({'type': 'ini_tags'})['values']:
                break
        else:
            raise Ux('server tag not found in db')
        self.account_configs = {}
        self.domain_configs = {}
        self.platform_configs = {}
        # create a wav directory if needed; the "for uri" loop below will check this directory for the existence
        # of a playback wav file for each uri each softphone account and create them if needed
        if not os.path.exists('wav'):
            os.mkdir('wav')
        for doc in db[platform_name].find():
            strdoc = CfgReader.stringify(doc)
            if strdoc['type'] == 'account' and context in strdoc['contexts']:
                self.account_configs[strdoc['uri']] = strdoc
            elif strdoc['type'] == 'domain':
                self.domain_configs[strdoc['name']] = strdoc
            elif strdoc['type'] == 'platform':
                self.platform_configs = strdoc
        re_sip = re.compile('sip:')
        re_num_dom = re.compile('sip:(([^@]*)@(.*))')
        for uri in self.account_configs.keys():
            account_config = self.account_configs[uri]
            uri = str(uri)
            m_sip = re_sip.match(uri)
            if m_sip:
                # if phone type not specified, set to 'soft '
                if 'phone_type' not in self.account_configs[uri]:
                    account_config['phone_type'] = 'soft'
                # if 'uri' matches re_sip, it is the registration uri
                # other tags not specified are set to None
                for _tag in ['password', 'proxy', 'scope', 'new_vms', 'target_uri', 'number', 'domain',
                             'saved_vms', 'deleted_vms', 'delete', 'name1', 'name2', 'conf_password']:
                    if _tag not in self.account_configs[uri]:
                        account_config[_tag] = None
                # conf_password is conf_pw in db, it's a legacy thing
                if 'conf_password' in self.account_configs[uri]:
                    account_config['conf_pw'] = account_config['conf_password']
                else:
                    account_config['conf_pw'] = None
                m_num_dom = re_num_dom.match(uri)
                if account_config['number'] is None:
                    if m_num_dom:
                        account_config['number'] = m_num_dom.group(2)
                    else:
                        raise Ux('%s: account number not specified' % uri)
                if account_config['domain'] is None:
                    if m_num_dom:
                        account_config['domain'] = m_num_dom.group(3)
                    else:
                        raise Ux('%s: account domain not specified' % uri)
                domain_config = self.domain_configs[account_config['domain']]
                for _tag in ['rs_user', 'rs_password', 'rs_domain']:
                    self.account_configs[uri][_tag] = domain_config[_tag]


def merge_dicts(dict1, dict2):
    """
        add items dict2 to dict2:

        for each attribute in dict2:
            if no attribute with that name in dict1:
                add attribute to dict1
            else:
                if dict1 attribute is instance of dict:
                    merge_dicts(<dict1 attribute>, <dict2 attribute>)
                else:
                    replace dict1 attribute with dict2 attribute

    :param dict1: dictionary with initial values, which will contain final merged values
    :param dict2: dictionary with values to merge into dict1
    """
    if not isinstance(dict1, dict):
        dict1 = {}
    if not isinstance(dict2, dict):
        dict2 = {}
    for key in dict2.keys():
        if key in dict1 and isinstance(dict1[key], dict):
            merge_dicts(dict1[key], dict2[key])
        else:
            dict1[key] = dict2[key]


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
            all_dbs[_db_name][collection_name] = db[collection_name]
    return all_dbs


def dump_dbs(_db_names, server, cfg_dir, _output_fd):
    all_dbs = read_dbs(_db_names, server)
    for _db_name in _db_names:
        _db = all_dbs[_db_name]
        db_dict = {}
        if _db_name.endswith("_accounts"):
            passwords = {}
        for collection_name in _db:
            db_dict[collection_name] = []
            collection = _db[collection_name]
            if _db_name.endswith("_accounts"):
                passwords[collection_name] = {}
            for item in collection.find():
                item.pop("_id")
                if _db_name.endswith("_accounts") and item['type'] == 'account':
                    passwords[collection_name][item["uri"]] = item.pop("password", None)
                db_dict[collection_name].append(item)
        if _output_fd:
            _output_fd.write("%s\n" % _db_name)
            _output_fd.write(json.dumps(db_dict, sort_keys=True, indent=4, separators=(',', ': ')))
            _output_fd.write('\n')
        else:
            with open(os.path.join(cfg_dir, '%s.json' % _db_name), 'w') as f:
                f.write(json.dumps(db_dict, sort_keys=True, indent=4, separators=(',', ': ')))
        if _db_name.endswith("_accounts"):
            if _output_fd:
                _output_fd.write("passwords\n")
                _output_fd.write(json.dumps(passwords, sort_keys=True, indent=4, separators=(',', ': ')))
                _output_fd.write('\n')
            else:
                with open(os.path.join(cfg_dir, 'passwords.json'), 'w') as f:
                    f.write(json.dumps(passwords, sort_keys=True, indent=4, separators=(',', ': ')))


def restore_db(_db_names, server, cfg_dir, _output_fd):
    all_output = {}
    all_collections = {}
    for _db_name in _db_names:
        with open(os.path.join(cfg_dir, '%s.json' % _db_name)) as infile:
            json_txt = infile.read()
        db_collections = json.loads(json_txt)
        all_output[_db_name] = db_collections
        all_passwords = None
        if _db_name.endswith("_site"):
            with open(os.path.join(cfg_dir, 'passwords.json')) as infile:
                json_txt = infile.read()
            all_passwords = json.loads(json_txt)
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
    ops = {'dump': dump_dbs, 'restore': restore_db}
    db_names = ['ccd_site']
    db_args = db_names + ['all']
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='  saves and restores databases from mongodb running on SERVER\n' +
                                                 '  using JSON files in config directory for database backup;\n'
                                                 '  "dump" gets <db_name> and saves in config/<db_name>.json\n' +
                                                 '  "restore" replaces <db_name> with data from config/<db_name>.json')
    parser.add_argument("-s", "--server", type=str, default='vqda',
                        help="(optional) specify mongodb server, default 'vqda'")
    parser.add_argument("-c", "--cfg_dir", type=str, default='config',
                        help="(optional) specify output directory, default 'config/mongo_json'")
    parser.add_argument("-o", "--output_file", default=None,
                        help="dump writes JSON to output file, restore writes JSON to output file,\n" +
                             "db and JSON files not changed; '-' for stdout")
    parser.add_argument("operation", type=str, choices=['dump', 'restore'], help="operation to perform")
    parser.add_argument("db_name", type=str, choices=db_args, help="name of database to dump or restore")
    args = parser.parse_args()
    if args.output_file is None:
        output_fd = None
    elif args.output_file == '-' or args.output_file == 'stdout':
        output_fd = sys.stdout
    else:
        output_fd = open(os.path.join(args.cfg_dir, args.output_file), 'w')
    if args.db_name == 'all':
        ops[args.operation](db_names, args.server, args.cfg_dir, output_fd)
    else:
        ops[args.operation]([args.db_name], args.server, args.cfg_dir, output_fd)
    if output_fd is not None and output_fd != sys.stdout:
        output_fd.close()
