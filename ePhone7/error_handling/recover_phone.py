from api import api
from mtaf import mtaf_logging
log = mtaf_logging.get_logger('mtaf.recover_phone')


def create_device():
    device_info = api.get_device_data()
    if device_info:
        log.debug("Device does exist")
    else:
        create_status = api.create_device()
        if create_status == 200:
            device_info = api.get_device_data()
            if device_info:
                log.debug("Device was created")
        else:
            log.debug("Device was not created")


create_device()