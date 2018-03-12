# -*- coding: utf-8 -*-
import MySQLdb
from twisted.enterprise import adbapi
from db.Config import CONFIG
from ScrapySpider.utils.log import Log


class DbException(Exception):
    """
    数据库自定义异常
    """
    pass


class DbHelper(object):
    """
    数据库操作类
    """

    def __init__(self):
        self.prefix = CONFIG.pop("table_prefix")
        # self.connect = MySQLdb.connect(**CONFIG)
        # self.connect.autocommit(True)
        self.pool = adbapi.ConnectionPool('MySQLdb', **CONFIG)

        # self.cursor = self.connect.cursor()
        pass

    def async_insert(self, table_name, params, update_params=list):
        """
        进行异步数据插入
        :param str table_name: 表名
        :param dict params: 参数
        :param update_params: 数据库存在主键，更新字段
        :return:
        """
        try:
            query = self.pool.runInteraction(self.__insert, table_name, params, update_params)
            query.addErrback(self.__handle_error)
        except DbException as e:
            Log.error("SQL 执行异常 DbHelper Line:40")
            return False

    def __handle_error(self, error):
        Log.error("async insert have an error：%s" % error)

    def __insert(self, cursor, table_name, params, update_params=list):
        """
        实际数据插入方法实现
        :param cursor: 游标
        :param str table_name: 表名
        :param dict params: 参数
        :return:
        """
        fields = ""
        values = ""
        if isinstance(params, dict):
            for k, v in params.items():
                fields += "`" + (str(k)) + "`,"
                values += "'" + str(v) + "',"
        else:
            Log.error("params need dict,you are %s" % str(type(params)))
            # raise DbException("params need dict,you are %s" % str(type(params)))

        update_values = ""
        if isinstance(update_params, list):
            for v in update_params:
                update_values += str(v) + "=VALUES(" + str(v) + "), "
            update_values = update_values.rstrip(", ")
        else:
            Log.error("update_params need list,you are %s" % str(type(update_params)))
            # raise DbException("update_params need list,you are %s" % str(type(update_params)))

        fields = fields.rstrip(",")
        values = values.rstrip(",")

        if update_values:
            sql = "insert into %s(%s)  values (%s)  ON DUPLICATE KEY UPDATE %s " % (
                self.prefix + table_name, fields, values, update_values)
        else:
            sql = "insert into %s(%s)  values (%s) " % (
                self.prefix + table_name, fields, values)
        try:
            affect_rows = cursor.execute(sql)
            Log.info("成功执行SQL语句：%s" % sql)
        except DbException as e:
            Log.error("SQL 语句执行异常：%s" % e)
            Log.error("SQL ：%s" % sql)
            affect_rows = 0

        # self.connect.commit()
        return affect_rows
        pass

    def update(self):
        pass

    def select(self):

        pass

    def delete(self):
        pass
