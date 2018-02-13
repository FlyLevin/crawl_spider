#!/usr/bin/python

try:
    from logging.handlers import RotatingFileHandler
    import logging.config

except ImportError as e:
    raise ImportError ('[%s] a module is missing.' % str[e])


logging.config.fileConfig("/home/user/crawl/logging.conf")
g_log = logging.getLogger()


# Init Log utility
def initLogger(log_file):
    ''' Init Log utility '''

    # mkdir
    os.system('mkdir -p %s' % os.path.dirname(log_file))
    _Formatter='%(asctime)s [%(process)d:%(thread)x] %(levelname)-8s[%(filename)s:%(lineno)d(%(funcName)s)] %(message)s'
    handler = RotatingFileHandler(filename=log_file, maxBytes=LOG_MAX_SIZE, backupCount=BACKUP_NUM)
    formatter = logging.Formatter(_Formatter)
    handler.setFormatter(formatter)
    loger = logging.getLogger()
    for hdlr in loger.handlers:
        hdlr.close()
        loger.removeHandler(hdlr)
    loger.setLevel(DEF_LOG_LEVEL)
    loger.addHandler(handler)

# set log level according to g_conf 
def setLogLevel(str_loglevel) :
    ''' set log level '''

    if str_loglevel == 'debug' :
        g_log.setLevel(logging.DEBUG)
    elif str_loglevel == 'info' :
        g_log.setLevel(logging.INFO)
    elif str_loglevel == 'warning' :
        g_log.setLevel(logging.WARN)
    else :
        g_log.setLevel(logging.ERROR)
