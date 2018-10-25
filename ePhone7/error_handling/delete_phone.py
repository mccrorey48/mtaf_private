from api import api
from mtaf import mtaf_logging
log = mtaf_logging.get_logger('mtaf.delete_phone')


def delete_device():
    device_info = api.get_device_data()
    if not device_info:
        log.debug("device does not exist")
    else:
        delete_status = api.delete_device_from_api()
        if delete_status == 200:
            device_info = api.get_device_data()
            if not device_info:
                log.debug("device was deleted")
        else:
            log.debug("device was not deleted")


def create_device():
    device_info = api.get_device_data()
    if device_info:
        log.debug("device does exist")
    else:
        create_status = api.create_device_from_api()
        if create_status == 200:
            device_info = api.get_device_data()
            if device_info:
                log.debug("device was created")
        else:
            log.debug("device was not created")


delete_device()

