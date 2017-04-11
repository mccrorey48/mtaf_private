import lib.logging_esi as logging
from lib.wrappers import Trace
from ePhone7.views.base import BaseView

log = logging.get_logger('esi.network_view')

class NetworkView(BaseView):
    locators = {
        "InvalidVlanId": {"by": "id", "value": "com.esi_estech.ditto:id/nw_warnings", "text": "Invalid VLAN identifier (1 ~ 4094)"},
        "InvalidVlanOk": {"by": "id", "value": "android:id/button1"},
        "InvalidVlanPriority": {"by": "id", "value": "com.esi_estech.ditto:id/nw_warnings", "text": "Invalid VLAN priority (0 ~ 7)"},
        "NetworkSaveAndReboot": {"by": "id", "value": "com.esi_estech.ditto:id/save_nw_config"},
        "NetworkSettingsBackButton": {"by": "id", "value": "com.esi_estech.ditto:id/back_button"},
        "NetworkSettingsLabel": {"by": "id", "value": "com.esi_estech.ditto:id/preferences_label", "text": "Network Settings"},
        "VlanDisable": {"by": "id", "value": "com.esi_estech.ditto:id/vlan_disable"},
        "VlanEnable": {"by": "id", "value": "com.esi_estech.ditto:id/vlan_enable"},
        "VlanRebootAlert": {"by": "id", "value": "com.esi_estech.ditto:id/count_down_label"},
        "VlanIdentifier": {"by": "id", "value": "com.esi_estech.ditto:id/nw_config_vlan_identifier_new_value"},
        "VlanPriority": {"by": "id", "value": "com.esi_estech.ditto:id/nw_config_vlan_priority_new_value"}
    }

    def __init__(self):
        super(NetworkView, self).__init__()

    @Trace(log)
    def verify_view(self):
        return len(self.find_named_elements('VlanDisable')) > 0


network_view = NetworkView()
