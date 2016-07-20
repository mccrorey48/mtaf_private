import lib.common.logging_esi as logging
log1 = logging.get_logger('esi.log1')
log2 = logging.get_logger('esi.log2')
log1.info("goodbye")
log2.info("hello")
logging.set_msg_src('just a test')
log1.info("world")
logging.set_msg_src('jat')
log1.info("goodbye")
log2.info("goodbye")

