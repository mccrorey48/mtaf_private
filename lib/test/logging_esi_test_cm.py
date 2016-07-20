from logging_esi_test2 import logit
import lib.common.logging_esi as logging_esi
import logging

# log = logging_esi.get_logger('esi.mm')
log = logging.getLogger('esi.mm')
log.info("logger-mm_ms-")


with logging_esi.msg_src_cm("src1"):
    log.info("logger-mm_ms-src1")

log.info("logger-mm_ms-popped")

log = logging_esi.get_logger('esi_test.xx')
log.info("logger-xx_ms-popped")

with logging_esi.msg_src_cm('jat'):
    log.info("logger-mm_ms-jat")
    log = logging_esi.get_logger('esi_test.xx')
    log.info("logger-xx_ms-jat")

with logging_esi.msg_src_cm('anothersrc'):
    log.info("logger-xx_ms-anothersrc")
    logit()


