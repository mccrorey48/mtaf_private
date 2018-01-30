from ccd.utils.configure import cfg
import ccd.views
from mock import Mock, patch
from mtaf import mtaf_logging
logging_esi.console_handler.setLevel(logging_esi.INFO)
log =mtaf_logging.get_logger('mtaf.reseller')


def make_mock(name):
    m = Mock()
    m.name = name
    return m


def make_mock_tree(name, subtree):
    root_mock = make_mock(name)
    for key in subtree:
        setattr(root_mock, key, make_mock_tree(key, subtree[key]))
    return root_mock


mock_features = [
        'Log in only allowed with valid user ID and password'
        ]

mock_views = {
    'login_view': {
        'find_named_element': {
            'return_value': {
                'send_keys': {},
                'click': {}
            },
        },
        'wait_for_invalid_login_alert': {}
    },
    'base_view': {
        'open_browser': {},
        'close_browser': {},
        'get_portal_url': {}
    },
    'reseller_view': {
        'wait_for_title': {},
        'click_named_element': {}
    }
}


def patches_start(context):
    context.mocks = {}
    for view in context.patches:
        context.mocks[view] = {}
        for op in context.patches[view]:
            context.mocks[view][op] = context.patches[view][op].start()
    context.mocks_started = True


def mock_reset_all(context):
    for view in context.mocks:
        for op in context.mocks[view]:
            if op != 'open_browser':
                context.mocks[view][op].reset_mock()


def patches_stop(context):
    for view in context.patches:
        for op in context.patches[view]:
            context.patches[view][op].stop()


def mock_assertions(context, scenario):
    open_browser = context.mocks['base_view']['open_browser']
    get_portal_url = context.mocks['base_view']['get_portal_url']
    find_element_by_key = context.mocks['login_view']['find_named_element']
    wait_for_title = context.mocks['reseller_view']['wait_for_title']
    assert open_browser.call_count == 1
    if scenario.name == 'Log in with valid user ID and password':
        assert get_portal_url.call_count == 1
        assert find_element_by_key.call_count == 3
        assert find_element_by_key.return_value.send_keys.call_count == 2
        username = find_element_by_key.return_value.send_keys.call_args_list[0][0][0]
        assert username == 'mmccroreyrs@SVAutoManage', "expect username 'mmccroreyrs@SVAutoManage', got %s" % username
        password = find_element_by_key.return_value.send_keys.call_args_list[1][0][0]
        assert password == '0222', "expect password '0222', got %s" % password
        assert wait_for_title.call_count == 1
        assert wait_for_title.call_args[0] == ('Manager Portal - Home',), \
            "expect 'Manager Portal - Home', got %s" % wait_for_title.call_args[0]
    elif scenario.name == 'Log in with valid user ID and invalid password':
        assert get_portal_url.call_count == 1
        assert find_element_by_key.call_count == 3
        assert find_element_by_key.return_value.send_keys.call_count == 2
        username = find_element_by_key.return_value.send_keys.call_args_list[0][0][0]
        assert username == 'mmccroreyrs@SVAutoManage', "expect username 'mmccroreyrs@SVAutoManage', got %s" % username
        password = find_element_by_key.return_value.send_keys.call_args_list[1][0][0]
        assert password == '2222', "expect password '2222', got %s" % password


def before_all(context):
    context.mocks_started = False
    if 'mock' in context.config.userdata:
        context.patches = {}
        for view in mock_views:
            context.patches[view] = {}
            for op in mock_views[view]:
                base_mock = make_mock_tree(op, mock_views[view][op])
                context.patches[view][op] = patch('ccd.views.%s.%s' % (view, op), base_mock)

        context.use_mocks = True
    else:
        context.use_mocks = False


def before_feature(context, feature):
    if context.use_mocks and feature.name in mock_features:
        patches_start(context)
    ccd_server = context.config.userdata.get('ccd_server')
    if 'cfg_server' in context.config.userdata:
        cfg_server = context.config.userdata.get('cfg_server')
    else:
        cfg_server = 'vqda'
    cfg.set_site(cfg_server, ccd_server)
    ccd.views.base_view.open_browser()


def before_scenario(context, scenario):
    context.scenario_name = scenario.name
    if context.mocks_started:
        mock_reset_all(context)


def before_step(context, step):
   mtaf_logging.push_msg_src("%s:%s" % (context.scenario.name, step.name))


def after_step(context, step):
   mtaf_logging.pop_msg_src()


def after_scenario(context, scenario):
    if context.mocks_started:
        mock_assertions(context, scenario)


def after_feature(context, feature):
    ccd.views.base_view.close_browser()
    if context.mocks_started:
            patches_stop(context)
