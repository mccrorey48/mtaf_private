from logging_esi_test2 import logit
import lib.common.logging_esi as logging_esi

if __name__ == '__main__':
    log = logging_esi.get_logger('esi.mm')
    log.info("logger-mm_ms-")
    logging_esi.push_msg_src('src1')
    log.info("logger-mm_ms-src1")
    logging_esi.pop_msg_src()
    log.info("logger-mm_ms-popped")
    log = logging_esi.get_logger('esi_test.xx')
    log.info("logger-xx_ms-popped")
    logging_esi.push_msg_src('jat')
    log.info("logger-mm_ms-jat")
    log = logging_esi.get_logger('esi_test.xx')
    log.info("logger-xx_ms-jat")
    logging_esi.push_msg_src('anothersrc')
    log.info("logger-xx_ms-anothersrc")
    logit()
