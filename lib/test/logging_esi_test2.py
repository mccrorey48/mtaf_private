import lib.common.logging_esi as logging


def logit():
    log = logging.get_logger('esi.sub')
    log.info("logger-sub_ms-")
    logging.push_msg_src('src3')
    log.info("logger-sub_ms-src3")
    logging.pop_msg_src()
    log.info("logger-sub_ms-popped")
