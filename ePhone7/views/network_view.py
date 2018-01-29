from mtaf import mtaf_logging
from mtaf.trace import Trace

from ePhone7.views.base_view import BaseView

log = mtaf_logging.get_logger('esi.network_view')


class NetworkView(BaseView):
    locators = {
        "InvalidVlanId": {"by": "-android uiautomator",
                          "value": "new UiSelector().textStartsWith(\"Invalid VLAN Identifier\")"},
        "InvalidVlanOk": {"by": "id", "value": "android:id/button1"},
        "InvalidVlanPriority": {"by": "-android uiautomator",
                                "value": "new UiSelector().textStartsWith(\"Invalid VLAN priority\")"},
        "NetworkSaveAndReboot": {"by": "id", "value": "com.esi_estech.ditto:id/save_nw_config"},
        "NetworkSettingsBackButton": {"by": "id", "value": "com.esi_estech.ditto:id/back_button"},
        "NetworkSettingsLabel": {"by": "id", "value": "com.esi_estech.ditto:id/preferences_label",
                                 "text": "Network Settings"},
        "VlanDisable": {"by": "id", "value": "com.esi_estech.ditto:id/vlan_disable"},
        "VlanEnable": {"by": "id", "value": "com.esi_estech.ditto:id/vlan_enable"},
        "VlanRebootAlert": {"by": "id", "value": "com.esi_estech.ditto:id/count_down_label"},
        "VlanIdentifier": {"by": "id", "value": "com.esi_estech.ditto:id/nw_config_vlan_identifier_new_value"},
        "VlanPriority": {"by": "id", "value": "com.esi_estech.ditto:id/nw_config_vlan_priority_new_value"}
    }

    def __init__(self):
        super(NetworkView, self).__init__()
        BaseView.network_view = self
        self.presence_element_names = ['NetworkSettingsLabel']

    @Trace(log)
    def verify_view(self):
        return len(self.find_named_elements('VlanDisable')) > 0


network_view = NetworkView()
