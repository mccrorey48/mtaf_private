from mtaf import mtaf_logging
from mtaf.trace import Trace
from mtaf.user_exception import UserException as Ux

from ePhone7.config.configure import cfg
from ePhone7.lib.utils.get_softphone import get_softphone
from ePhone7.views.user_view import UserView

from time import sleep

log = mtaf_logging.get_logger('mtaf.history_view')


class HistoryView(UserView):
    locators = {
        "All": {"by": "id", "value": "com.esi_estech.ditto:id/all_history_btn"},
        "CallerName": {"by": "id", "value": "com.esi_estech.ditto:id/callerName"},
        "CallerTime": {"by": "id", "value": "com.esi_estech.ditto:id/calledTime"},
        "CallerNumber": {"by": "id", "value": "com.esi_estech.ditto:id/callerNumber"},
        "CallIcon": {"by": "id", "value": "com.esi_estech.ditto:id/call_type_button"},
        "CallIcon1": {"by": "zpath", "value": "//rv/rl[1]/bt"},
        "Missed": {"by": "id", "value": "com.esi_estech.ditto:id/missed_call_history_btn"},
        "HistoryParent": {"by": "zpath", "value": "//rv/rl"},
        "HistoryParent1": {"by": "zpath", "value": "//rv/rl[1]"},
        # "History1Texts": {"by": "zpath", "value": "(//rv/rl[1])/tv"},
    }

    def __init__(self):
        super(HistoryView, self).__init__()
        self.tab_names = ('All', 'Missed')
        self.png_file_base = 'history'
        self.presence_element_names = ['Missed']

    @Trace(log)
    def call_contact_test(self):
        src_name = cfg.site['DefaultSoftphoneUser']
        elems = self.find_named_elements('CallerName')
        self.assertGreater(len(elems), 0, 'No CallerName elements found')
        name_elem = elems[0]
        name = name_elem.text
        expected = src_name
        self.assertEqual(name, expected, "First caller name expected %s, actual %s" % (expected, name))
        loc_y = name_elem.location['y']
        log.debug("first name location y = %s" % loc_y)
        entry_elems = history_view.find_named_elements('HistoryParent')
        for i, entry_elem in enumerate(entry_elems[:-1]):
            if entry_elems[i].location['y'] < loc_y < entry_elems[i+1].location['y']:
                entry_elem = entry_elems[i]
                break
        else:
            raise Ux('No HistoryEntry element found in same row as first CallerName element')
        log.debug("history entry location y = %s" % entry_elem.location['y'])
        call_icon = history_view.find_named_sub_element(entry_elem, 'CallIcon')
        log.debug("call icon location y = %s" % call_icon.location['y'])
        softphone = get_softphone()
        softphone.account_info.incoming_response = 200
        self.click_element(call_icon)
        softphone.wait_for_call_status('call', 20)
        sleep(10)
        softphone.end_call()

    @Trace(log)
    def get_top_record_parent(self):
        parent_top = self.find_named_element('HistoryParent1')
        # caller_name = self.find_named_sub_element(parent_top, 'CallerName').text
        # log.debug('<%s> subelement CallerName text = %s' % (parent_top.id, caller_name))
        caller_time = self.find_named_sub_element(parent_top, 'CallerTime').text
        log.debug('<%s> subelement CallerTime text = %s' % (parent_top.id, caller_time))
        # caller_number = self.find_named_sub_element(parent_top, 'CallerNumber').text
        # log.debug('<%s> subelement CallerNumber text = %s' % (parent_top.id, caller_number))
        time = dict(zip(['quantity', 'type', 'null'], caller_time.split()[0:]))
        log.debug('quantity  = %s' % time['quantity'])
        log.debug('type  = %s' % time['type'])
        # if time['quantity'] == '0':
        #     log.info('quantity is 0')
        #     return True
        # "in 0 minutes" is know bug so this is a workaround while they fix this
        if caller_time == "in 0 minutes" or time['quantity'] == '0':
            log.info('quantity is not 0')
            return True
        return False

    @Trace(log)
    def get_top_call_record(self):
        self.wait_for_condition_true(self.get_top_record_parent, lambda: 'no correct recent record', timeout=60)

    @Trace(log)
    def ignore_step(self):
        pass

    @Trace(log)
    def the_expect_icon_is_displayed(self, handset_color):
        handset_color_dic = {'blue': [99, 139, 237, 275],
                             'green': [79, 187, 110, 264],
                             'red': [216, 82, 81, 256]}
        if handset_color not in handset_color_dic:
            raise Ux('not color %s' % handset_color)
        handset_button = self.find_named_element('CallIcon1')
        expect_color = handset_color_dic[handset_color]
        log.info('expected_count = %s', expect_color)
        history_view.get_screenshot_as_png('headset')
        actual_color = self.get_element_color_and_count('headset', handset_button, color_list_index=2)
        log.info('actual_count = %s', actual_color)
        return actual_color == expect_color

    @Trace(log)
    def get_expect_icon_color(self, handset_color):
        self.wait_for_condition_true((lambda: self.the_expect_icon_is_displayed(handset_color)),
                                     lambda: 'no correct icon color', timeout=60)

    @Trace(log)
    def touch_handset(self):
        elem = self.find_named_element("CallIcon1")
        if elem is None:
            raise Ux("no matching element found")
        else:
            elem.click()
        return True


history_view = HistoryView()
