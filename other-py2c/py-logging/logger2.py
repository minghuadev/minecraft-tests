#!/usr/bin/env python

import logging
import logging.handlers
import datetime
import threading
import io


_conf_logger_handlers_added = {}
_conf_lock = threading.Lock()


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        now = datetime.datetime.now()
        dtStr = now.strftime("%H:%M:%S")
        result = dtStr + "::" + super().formatException(exc_info)
        return repr(result)

    def format(self, record):
        now = datetime.datetime.now()
        #dtStr = now.strftime("%Y-%m-%d-%H:%M:%S")
        dtStr = now.strftime("%H:%M:%S")
        result = dtStr + "::" + super().format(record)
        if record.exc_text:
            result = result.replace("\n", "")
        return result


def init_stdout_or_file(log_file=None, debug=False, facility=None):
    if log_file is None:
        handler = logging.StreamHandler()
    else:
        handler = logging.handlers.RotatingFileHandler(log_file,
                                                       maxBytes=2000*1000,
                                                       backupCount=7)
    formatter = OneLineExceptionFormatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    if facility is None:
        lgr = logging.getLogger()
    else:
        lgr = logging.getLogger(facility)
    if debug is None:
        #root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
        lgr.setLevel("INFO")
    else:
        lgr.setLevel("DEBUG")

    global _conf_logger_handlers_added
    _conf_lock.acquire()
    is_added = _conf_logger_handlers_added.get(log_file, None)
    if not is_added:
        _conf_logger_handlers_added[log_file] = True
        _conf_lock.release()
        lgr.addHandler(handler)
    else:
        _conf_lock.release()
    #print("logger facility ", facility, " debug ", debug)

#try:
#    exit(main())
#except Exception:
#    logging.exception("Exception in main(): ")
#    exit(1)


class Logger(object):

    count_warn = 0
    count_err  = 0
    count_crit = 0

    @classmethod
    def class_count_clear(cls):
        Logger.count_warn = 0
        Logger.count_err  = 0
        Logger.count_crit = 0

    @classmethod
    def class_count_get(cls):
        return [Logger.count_warn,
                Logger.count_err,
                Logger.count_crit]

    def __init__(self, log_facility=None):
        if log_facility is None:
            facility = None
        else:
            facility = log_facility
        self._logr = logging.getLogger(facility)

    def logdbg(self, *args, **kwargs):
        fake_file = io.StringIO()
        print(*args, **kwargs, file=fake_file)
        self._logr.debug(fake_file.getvalue())

    def loginfo(self, *args, **kwargs):
        self._logr.info(*args, **kwargs)

    def logwarn(self, *args, **kwargs):
        self._logr.warning(*args, **kwargs)
        Logger.count_warn += 1

    def logerr(self, *args, **kwargs):
        self._logr.error(*args, **kwargs)
        Logger.count_err += 1

    def logcrit(self, *args, **kwargs):
        self._logr.critical(*args, **kwargs)
        Logger.count_crit += 1


