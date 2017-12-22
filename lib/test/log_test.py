import lib.mtaf_logging as logging
log = logging.get_logger('mtaf.log_test')
logging.console_handler.setLevel(logging.INFO)
log.debug("debug message")
log.trace("trace message")
log.info("info message")
log.warn("warn message")
