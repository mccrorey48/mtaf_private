from behave import *
from ePhone7.views import *
import re
from time import sleep


@step("[network] I enter a VLAN identifier greater than 4094")
def network_i_enter_a_vlan_identifier_greater_than_4094(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_view.find_named_element('VlanIdentifier').clear()
        network_view.send_keycode('KEYCODE_4')
        network_view.send_keycode('KEYCODE_0')
        network_view.send_keycode('KEYCODE_9')
        network_view.send_keycode('KEYCODE_5')
        network_view.send_keycode('KEYCODE_BACK')


@step("[network] I enter a VLAN priority between 0 and 7")
def network_i_enter_a_vlan_priority_between_0_and_7(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_view.find_named_element('VlanPriority').clear()
        network_view.send_keycode('KEYCODE_3')
        network_view.send_keycode('KEYCODE_BACK')


@then('[network] I see an "Invalid VLAN Identifier" alert')
def network_i_see_an_invalid_vlan_identifier_alert(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert network_view.element_is_present('InvalidVlanId'), "Expected Invalid VLAN Identifier alert"


@step("[network] I see the Network Settings view")
def network_i_see_the_network_settings_view(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert network_view.element_is_present('NetworkSettingsLabel')


@when('[network] I touch "OK" on the "Invalid VLAN Identifier" alert')
def network_i_touch_ok_on_the_invalid_vlan_identifier_alert(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_view.click_named_element('InvalidVlanOk')


@step('[network] I touch "Save and Reboot"')
def network_i_touch_save_and_reboot(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_view.click_named_element('NetworkSaveAndReboot')
        pass


@step("[network] I touch the back arrow at the top of the Network Settings view")
def network_i_touch_the_back_arrow_at_the_top_of_the_network_settings_view(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_view.click_named_element('NetworkSettingsBackButton')


@step("[network] the Disable button is active")
def network_the_disable_button_is_active(context):
    if 'fake' not in str(context._config.tags).split(','):
        elem = network_view.find_named_element('VlanDisable')
        assert elem.get_attribute('checked') == 'true'


@step("[network] the Disable button is inactive")
def network_the_disable_button_is_inactive(context):
    if 'fake' not in str(context._config.tags).split(','):
        elem = network_view.find_named_element('VlanDisable')
        assert elem.get_attribute('checked') == 'false'


@step("[network] the Enable button is active")
def network_the_enable_button_is_active(context):
    if 'fake' not in str(context._config.tags).split(','):
        elem = network_view.find_named_element('VlanEnable')
        assert elem.get_attribute('checked') == 'true'


@step("[network] the Enable button is inactive")
def network_the_enable_button_is_inactive(context):
    if 'fake' not in str(context._config.tags).split(','):
        elem = network_view.find_named_element('VlanEnable')
        assert elem.get_attribute('checked') == 'false'


@step("[network] The reboot alert window appears")
def network_the_reboot_alert_window_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert network_view.element_is_present("VlanRebootAlert")
