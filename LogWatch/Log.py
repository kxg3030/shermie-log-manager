import logging
import time
from logging.handlers import TimedRotatingFileHandler

from rich.logging import RichHandler


class Log(object):
    _instance = None
    writer = None
    logger = None

    def __init__(self):
        pass

    @classmethod
    def Instance(cls, *args, **kwargs):
        if Log._instance is None:
            instance = Log(*args, **kwargs)
            instance.Init()
            Log._instance = instance
        return Log._instance

    def Init(self):
        formater = logging.Formatter('%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d]  %(message)s')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logName = "Runtime/" + time.strftime("%Y-%m-%d", time.localtime(int(time.time()))) + ".log"
        stdHandler = logging.StreamHandler()
        stdHandler.setLevel(logging.DEBUG)
        logger.addHandler(stdHandler)

        fileHandler = TimedRotatingFileHandler(logName, when='MIDNIGHT', interval=1, backupCount=30, encoding="utf-8")
        fileHandler.setLevel(logging.INFO)
        fileHandler.setFormatter(formater)
        logger.addHandler(fileHandler)
        self.logger = logger
