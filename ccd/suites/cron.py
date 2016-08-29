import lib.common.logging_esi as logging_esi
logging_esi.console_handler.setLevel(logging_esi.INFO)
log = logging_esi.get_logger('esi.ccd_cron')
with logging_esi.msg_src_cm('importing modules'):
    import unittest
    from lib.common.wrappers import TestCase
    from lib.web.actions import Actions
