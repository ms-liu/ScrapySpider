# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

import os
from scrapy.pipelines.images import ImagesPipeline

from db.DbHelper import DbHelper
from items import BaseItem
from utils.log import Log


class DBPipeline(object):
    """
    数据库操作Pipeline
    """

    def __init__(self):
        """
        创建DbHelper对象
        """
        self.helper = DbHelper()

    def process_item(self, item, spider):
        """
        解析Item
        :param item:
        :param spider:
        :return:
        """
        if isinstance(item, BaseItem):
            # 异步数据插入
            try:
                table_name, params, update_params = item.render_insert_info()
                self.helper.async_insert(table_name, params, update_params)
            except Exception as e:
                Log.error("Item组装异常：%s" % e)
                Log.error("当前ITEM：%s" % item)
        else:
            pass
        return item


class LoadImagePipeline(ImagesPipeline):
    """
    图片下载Pipeline
    """

    def item_completed(self, results, item, info):
        """
        Item准备完毕
        :param results:
        :param item:
        :param info:
        :return:
        """
        global path_local
        for tag, value in results:
            path_local = value['path']
        # BASE_STORE = os.path.join(os.path.dirname(__file__), "data")
        if path_local:
            year, month, day = str(datetime.date.today()).split("-")
            item['cover_local'] = os.path.join(year, month, day, path_local)
        return item
