from behave import *
from eConsole.views import *
from eConsole.config.configure import cfg


@step('I click the Login button')
def i_click_the_login_button(context):
    login_view.click_login_button()


@step('I enter a valid {user_scope} password')
def i_enter_a_valid_userscope_password(context, user_scope):
    user = cfg.default_user[user_scope]
    password = cfg.accounts[user]['password']
    login_view.input_password(password)


@step('I enter a valid {user_scope} user ID')
def i_enter_a_valid_userscope_user_id(context, user_scope):
    user = cfg.default_user[user_scope]
    login_view.input_username(user)


@step('I go to the portal login page')
def i_go_to_the_portal_login_page(context):
    base_view.get_url(cfg['portal_url'][context.config.userdata['portal_server']])


@step("my name is displayed in the upper right corner")
def my_name_is_displayed_in_the_upper_right_corner(context):
    user = cfg.accounts[cfg.default_user[context.config.userdata['user_scope']]]
    expect_text = ' '.join([user[key] for key in ['name1', 'name2', 'password']])
    main_button_text = base_view.MainButton.text
    assert main_button_text == expect_text, "main button text is %s, expected %s" % (
        main_button_text, expect_text)


@step("the {expected_name} tab is selected")
def the_expectedname_tab_is_selected(context, expected_name):
    selected_tab_text = base_view.SelectedTab.text
    assert selected_tab_text == expected_name, "selected tab text is %s, expected %s" % (
        selected_tab_text, expected_name)


