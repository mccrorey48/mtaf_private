import sys
import traceback
import mtaf_logging


log = mtaf_logging.get_logger('mtaf.decorators')


def fake(func):
    def wrapper(context, *args, **kwargs):
        if 'fake' in str(context._config.tags).split(','):
            pass
            # sleep(0.1)
        else:
            try:
                func(context, *args, **kwargs)
            except BaseException as e:
                (exc_type, value, tb) = sys.exc_info()
                file, line, fn, cmd = traceback.extract_tb(tb)[-1]
                log.warn('EXCEPTION: %s - %s in %s:%s:%s "%s"' %
                         (exc_type.__name__, value, file, fn, line, cmd))
                raise e

    return wrapper

