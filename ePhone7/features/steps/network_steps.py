from behave import *
from ePhone7.views import *
from lib.wrappers import fake


@step("[network] I enter a valid VLAN identifier")
@fake
def network__i_enter_a_valid_vlan_identifier(context):
    context.run_substep("[network] I enter 20 as a VLAN identifier")


@step("[network] I enter a valid VLAN priority")
@fake
def network__i_enter_a_valid_vlan_priority(context):
    context.run_substep("[network] I enter 0 as a VLAN priority")


@step("[network] I enter a VLAN identifier between 1 and 4094")
@fake
def network__i_enter_a_vlan_identifier_between_1_and_4094(context):
    context.run_substep("[network] I enter 20 as a VLAN identifier")


@step("[network] I enter a VLAN identifier greater than 4094")
@fake
def network__i_enter_a_vlan_identifier_greater_than_4094(context):
    context.run_substep("[network] I enter 4095 as a VLAN identifier")


@step("[network] I enter a VLAN priority between 0 and 7")
@fake
def network__i_enter_a_vlan_priority_between_0_and_7(context):
    context.run_substep("[network] I enter 0 as a VLAN priority")


@step("[network] I enter a VLAN priority greater than 7")
@fake
def network__i_enter_a_vlan_priority_greater_than_7(context):
    context.run_substep("[network] I enter 8 as a VLAN priority")


@step("[network] I enter {id} as a VLAN identifier")
@fake
def network__i_enter_id_as_a_vlan_identifier(context, id):
    network_view.find_named_element('VlanIdentifier').clear()
    network_view.send_keycode_back()
    for digit in [int(c) for c in id]:
        network_view.send_keycode_number(digit)


@step("[network] I enter {priority} as a VLAN priority")
@fake
def network__i_enter_id_as_a_vlan_priority(context, priority):
    network_view.find_named_element('VlanPriority').clear()
    network_view.send_keycode_back()
    for digit in [int(c) for c in priority]:
        network_view.send_keycode_number(digit)


@step('[network] I see an "Invalid VLAN Identifier" alert')
@fake
def network__i_see_an_invalid_vlan_identifier_alert(context):
    assert network_view.element_is_present('InvalidVlanId'), "Expected Invalid VLAN Identifier alert"


@step("[network] I see the Network Settings view")
@fake
def network__i_see_the_network_settings_view(context):
    assert network_view.element_is_present('NetworkSettingsLabel')


@step("[network] I see the VLAN controls")
@fake
def network__i_see_the_vlan_controls(context):
    assert network_view.element_is_present('VlanEnable')
    assert network_view.element_is_present('VlanDisable')


@step("[network] I touch the back arrow at the top of the Network Settings view")
@fake
def network__i_touch_the_back_arrow_at_the_top_of_the_network_settings_view(context):
    network_view.click_named_element('NetworkSettingsBackButton')


@step("[network] I touch the VLAN Disable button")
@fake
def network__i_touch_the_vlan_disable_button(context):
    network_view.click_named_element('VlanDisable')


@step("[network] I touch the VLAN Enable button")
@fake
def network__i_touch_the_vlan_enable_button(context):
    network_view.click_named_element('VlanEnable')


@step("[network] the Disable button is active")
@fake
def network__the_disable_button_is_active(context):
    elem = network_view.find_named_element('VlanDisable')
    assert elem.get_attribute('checked') == 'true'


@step("[network] the Disable button is inactive")
@fake
def network__the_disable_button_is_inactive(context):
    elem = network_view.find_named_element('VlanDisable')
    assert elem.get_attribute('checked') == 'false'


@step("[network] the Enable button is active")
@fake
def network__the_enable_button_is_active(context):
    elem = network_view.find_named_element('VlanEnable')
    assert elem.get_attribute('checked') == 'true'


@step("[network] the Enable button is inactive")
@fake
def network__the_enable_button_is_inactive(context):
    elem = network_view.find_named_element('VlanEnable')
    assert elem.get_attribute('checked') == 'false'


@step("[network] The reboot alert window appears")
@fake
def network__the_reboot_alert_window_appears(context):
    assert network_view.element_is_present("VlanRebootAlert")


