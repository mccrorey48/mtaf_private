"""
    Call processing tests for the ESI Hosted PBX
    
    Performs tests by creating soft phones using the pjsip/pjsua libraries via a Python pjsua API.
    
    This module accesses the Python pjsua API by importing the wrapper module pjsua_lib.
    
    Also imported:
        wf       -   for capturing wav files
        audioop  -   to measure RMS audio energy from wav file data
        goertzel -   to detect DTMF audio sequences in recorded audio
        
"""
import re
import lib.common.logging_esi as logging
from pymongo import MongoClient
from lib.common.user_exception import UserException as Ux
import os
from lib.softphone.wav_audio import create_wav_file

log = logging.get_logger('esi.cfg_reader')


class CfgReader:
    account_configs = {}
    locators = {}
    platform_configs = {}
    domain_configs = {}
    vm_caller_account_configs = {}
    vm_caller_configs = {}
    pbfile_strings = {}
    platform_names = ['production', 'svlab', 'asterisk']

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
        db = self.client.test_accounts
        if platform_name in self.platform_names:
            return db[platform_name].find_one({"type": "ini_tags"})['values']

    def merge_dicts(self, dict1, dict2):
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
                self.merge_dicts(dict1[key], dict2[key])
            else:
                dict1[key] = dict2[key]

    def read_locators_from_db(self, svr_tag):
        db = self.client.ccd_locators
        self.locators['xpath'] = CfgReader.stringify(db.default.find_one({'type': 'xpath'}))
        self.merge_dicts(self.locators['xpath'], CfgReader.stringify(db[svr_tag].find_one({'type': 'xpath'})))
        self.locators['javascript'] = CfgReader.stringify(db.default.find_one({'type': 'javascript'}))
        self.merge_dicts(self.locators['javascript'], CfgReader.stringify(db[svr_tag].find_one({'type': 'javascript'})))
        pass

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
        db = self.client.test_accounts
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
                             'saved_vms', 'deleted_vms', 'delete', 'name2', 'conf_password']:
                    if _tag not in self.account_configs[uri]:
                        account_config[_tag] = None
                # conf_password is conf_pw in db, it's a legacy thing
                if 'conf_password' in self.account_configs[uri]:
                    account_config['conf_pw'] = account_config['conf_password']
                else:
                    account_config['conf_pw'] = None
                # For calling targets, use sip:<number>@<domain>.
                # if these entries are not present then attempt to
                # extract them from the uri; if the uri is not in
                # <number>@<domain> format then the number and domain
                # formats need to be present
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
                # for softphone accounts, set a value for the playback filename that identifies the account
                # using voice or dtmf audio; then if the needed wav file doesn't exist, create it
                if account_config['phone_type'] == 'soft':
                    if use_dtmf_audio:
                        self.pbfile_strings[uri] = 'wav/dtmf_%s.wav' % account_config['number']
                    else:
                        self.pbfile_strings[uri] = 'wav/%s.wav' % account_config['number']
                    if not os.path.exists(self.pbfile_strings[uri]):
                        create_wav_file(self.pbfile_strings[uri])
                domain_config = self.domain_configs[account_config['domain']]
                for _tag in ['rs_user', 'rs_password', 'rs_domain']:
                    self.account_configs[uri][_tag] = domain_config[_tag]
