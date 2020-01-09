# -*- coding: utf-8 -*-
import logging
import time


class Logger(object):
    """
    终端打印不同颜色的日志，在pycharm中如果强行规定了日志的颜色， 这个方法不会起作用， 但是
    对于终端，这个方法是可以打印不同颜色的日志的。
    """

    # 在这里定义StreamHandler，可以实现单例， 所有的logger()共用一个StreamHandler
    ch = logging.StreamHandler()

    def __init__(self):
        # 定义日志
        curdate = time.strftime("%Y%m%d")
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(filename='proxyip-%s.log' % (curdate), level=logging.DEBUG, format=LOG_FORMAT)
        self.logger = logging.getLogger()

    def debug(self, message):
        self.fontColor('\033[0;32m%s\033[0m')
        self.logger.debug(message)

    def info(self, message):
        self.fontColor('\033[0;34m%s\033[0m')
        self.logger.info(message)

    def warning(self, message):
        self.fontColor('\033[0;37m%s\033[0m')
        self.logger.warning(message)

    def error(self, message):
        self.fontColor('\033[0;31m%s\033[0m')
        self.logger.error(message)

    def critical(self, message):
        self.fontColor('\033[0;35m%s\033[0m')
        self.logger.critical(message)

    def fontColor(self, color):
        # 不同的日志输出不同的颜色
        formatter = logging.Formatter(color % '[%(asctime)s] - [%(levelname)s] - %(message)s')
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.ch)
