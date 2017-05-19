from time import sleep

import lib.logging_esi as logging
from ePhone7.config.configure import cfg
from ePhone7.utils.get_softphone import get_softphone
from ePhone7.views.user import UserView
from lib.user_exception import UserException as Ux
from lib.wrappers import Trace

log = logging.get_logger('esi.history_view')


class HistoryView(UserView):
    locators = {
        "All": {"by": "id", "value": "com.esi_estech.ditto:id/button1", "text": "All"},
        "CallerName": {"by": "id", "value": "com.esi_estech.ditto:id/callerName"},
        "CallIcon": {"by": "id", "value": "com.esi_estech.ditto:id/call_type_button"},
        "Missed": {"by": "id", "value": "com.esi_estech.ditto:id/button2", "text": "Missed"},
        "HistoryEntry": {"by": "zpath", "value": "//rv/rl"},
        "HistoryList": {"by": "id", "value": "com.esi_estech.ditto:id/call_history_sliding_layout"}
    }

    def __init__(self):
        super(HistoryView, self).__init__()
        self.tab_names = ('All', 'Missed')
        self.png_file_base = 'history'

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
        entry_elems = history_view.find_named_elements('HistoryEntry')
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
        self.click_named_element('EndActiveCall')
        softphone.wait_for_call_status('idle', 20)


history_view = HistoryView()

