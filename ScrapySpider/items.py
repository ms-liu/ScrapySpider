# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime

import scrapy
import time
import re

from scrapy.loader.processors import MapCompose, Join


def reg_matcher(food, regular, *default_value):
    if isinstance(food, list):
        food = food[0]
    result = re.match(regular, food,re.S)
    if result:
        return result.group(1)

    return (lambda: "" if default_value is None else default_value)()


def handle_date(date):
    """
    处理日期
    :param date:
    :return:
    """
    result = 0
    if "天" in date:
        match_result = re.match("(\d+)", date)
        days = lambda: int(match_result.group(1)) if match_result else 1
        result = datetime.date.today() - datetime.timedelta(days=days())
        # dateTime = time.strptime(dateTime.strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
        result = int(time.mktime(result.timetuple()))
    elif ":" in date:
        result = int(
            time.mktime(time.strptime((datetime.date.today().strftime("%Y-%m-%d ") + date), "%Y-%m-%d %H:%M")))
    elif "-" in date:
        result = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
    else:
        result = int(time.time())
    return result


class BaseItem(scrapy.Item):
    """
    基础数据处理Item
    """

    def render_insert_info(self):
        """
        用于返回SQL语句，以及参数值
        :return: SQL,params
        """
        table_name = """"""
        params = ()
        update_params = []
        return table_name, params, update_params


class FilterJoin(Join):
    def __init__(self, filter_regular, separator=u' '):
        super().__init__(separator)
        self.separator = separator
        self.filter = filter_regular

    def __call__(self, values):
        return self.separator.join(list(filter(lambda y: self.filter(y), values)))


class JobItem(BaseItem):
    """
    工作Item
    """

    url = scrapy.Field()
    url_id = scrapy.Field(
        input_processor=MapCompose(lambda x: reg_matcher(x, ".*?(\d+).*"))
    )
    title = scrapy.Field()
    salary_min = scrapy.Field(
        input_processor=MapCompose(lambda x: reg_matcher(x, ".*?(\d+).*", 0) if "-" in x else 0)
    )
    salary_max = scrapy.Field(
        input_processor=MapCompose(
            lambda x: reg_matcher(x, ".*-(\d+)?(k|K)", 0) if "-" in x else 0)
    )
    exp_min = scrapy.Field(
        input_processor=MapCompose(lambda x: reg_matcher(x, ".*?(\d+).*", 0) if "-" in x else 0)
    )
    exp_max = scrapy.Field(
        input_processor=MapCompose(
            lambda x: reg_matcher(x, ".*-(\d+)?(年|$)", 0) if "-" in x else 0)
    )
    degree = scrapy.Field(
        input_processor=MapCompose(lambda x: reg_matcher(x, ".*?([\u4E00-\u9FA5]+).*"))
    )
    type = scrapy.Field(
        input_processor=MapCompose(lambda x: reg_matcher(x, ".*?([\u4E00-\u9FA5]+).*"))
    )
    date = scrapy.Field(
        input_processor=MapCompose(
            lambda x: handle_date(reg_matcher(x, ".*?((\d+天前)|(\d+:\d+)|(\d{4}[年/-]\d+($|[月/-])\d*($|[号日]|)))"))
        )
    )
    tags = scrapy.Field(output_processor=Join(","))
    advantages = scrapy.Field()
    desc = scrapy.Field(output_processor=Join(";"))
    location = scrapy.Field(output_processor=FilterJoin(lambda x: "地图" not in x, ","))
    company_url = scrapy.Field()
    company_name = scrapy.Field(input_processor=MapCompose(lambda x: reg_matcher(x, ".*?([\S]+).*", "")))
    crawl_time = scrapy.Field()

    def render_insert_info(self):
        table_name = "job"
        params = dict(
            url=self['url'],
            url_id=self['url_id'],
            title=self['title'],
            salary_min=self['salary_min'],
            salary_max=self['salary_max'],
            exp_min=self['exp_min'],
            exp_max=self['exp_max'],
            degree=self['degree'],
            type=self['type'],
            date=self['date'],
            tags=self['tags'],
            advantages=self['advantages'],
            desc=self['desc'],
            location=self['location'],
            company_url=self['company_url'],
            company_name=self['company_name'],
            crawl_time=self['crawl_time'],
            crawl_update_time=int(time.time()),
        )
        update_params = [
            'salary_min',
            'salary_max',
            'exp_min',
            'exp_max',
            'degree',
            'location',
            "crawl_update_time"
        ]
        return table_name, params, update_params
