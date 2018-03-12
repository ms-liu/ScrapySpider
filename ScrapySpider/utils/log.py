# -*- coding: utf-8 -*-
import pickle
import os
import sys
import codecs


class Log(object):
    NONE = 0
    WARNING = 1
    ERROR = 2
    LOG = 3

    log_level = ERROR
    BASE_LOG_DIR = os.path.abspath(__package__) + "/../runtime/log/"

    @staticmethod
    def log(msg):
        info_file = codecs.open(Log.BASE_LOG_DIR + "log", "a+b", 'utf-8')
        if Log.log_level > Log.NONE:
            info_file.write(" [Log] ：" + msg + "\n")
            info_file.close()

    @staticmethod
    def info(msg):
        """
        :param str msg:
        :return:
        """
        info_file = codecs.open(Log.BASE_LOG_DIR + "info", "a+b", 'utf-8')
        info_file.write(" [Information] ：" + msg + "\n")
        info_file.close()
        pass

    @staticmethod
    def warning(msg):
        """
        :param str msg:
        :return:
        """
        info_file = codecs.open(Log.BASE_LOG_DIR + "warning", "a+b", 'utf-8')
        info_file.write(" [Warning] ：" + msg + "\n")
        info_file.close()
        pass

    @staticmethod
    def error(msg):
        """
        :param str msg:
        :return:
        """
        info_file = codecs.open(Log.BASE_LOG_DIR + "error", "a+b", 'utf-8')
        info_file.write(" [Error] ：" + msg + "\n")
        info_file.close()
        pass
