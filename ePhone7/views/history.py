from time import sleep

import lib.common.logging_esi as logging
from ePhone7.utils.configure import cfg
from ePhone7.views.user import UserView
from lib.common.user_exception import UserException as Ux
from lib.common.wrappers import Trace
from lib.softphone.softphone import get_softphone

log = logging.get_logger('esi.contacts_view')


class HistoryView(UserView):

    @Trace(log)
    def __init__(self):
        super(HistoryView, self).__init__()
        self.tab_names = ('All', 'Missed')
        self.png_file_base = 'history'

    @Trace(log)
    def call_contact_test(self):
        src_name = cfg.site['DefaultSoftphoneUser']
        elems = self.actions.find_elements_by_key('CallerName')
        self.actions.assertGreater(len(elems), 0, 'No CallerName elements found')
        name_elem = elems[0]
        name = name_elem.text
        expected = src_name
        self.actions.assertEqual(name, expected, "First caller name expected %s, actual %s" % (expected, name))
        loc_y = name_elem.location['y']
        log.debug("first name location y = %s" % loc_y)
        entry_elems = history_view.actions.find_elements_by_key('HistoryEntry')
        for i, entry_elem in enumerate(entry_elems[:-1]):
            if entry_elems[i].location['y'] < loc_y < entry_elems[i+1].location['y']:
                entry_elem = entry_elems[i]
                break
        else:
            raise Ux('No HistoryEntry element found in same row as first CallerName element')
        log.debug("history entry location y = %s" % entry_elem.location['y'])
        call_icon = history_view.actions.find_sub_element_by_key(entry_elem, 'CallIcon')
        log.debug("call icon location y = %s" % call_icon.location['y'])
        softphone = get_softphone()
        self.actions.click_element(call_icon.click)
        softphone.wait_for_call_status('start', 20)
        sleep(10)
        self.actions.click_element_by_key('EndActiveCall')
        softphone.wait_for_call_status('end', 20)


history_view = HistoryView()

