# -*- coding: utf-8 -*-

from utils.log import Log
import re
import os
import sys

# print(os.path.abspath(__package__))
# str = "https://www.lagou.com/jobs/3183990.html?source=home_hot&i=home_hot-0"
# str = "https://www.lagou.com/jobs/3183990.html?source=home_hot&i=home_hot-0"
import time
import datetime

str = '1天前\xa0 发布于拉勾网'
str = '09:04\xa0 发布于拉勾网'
str = '2018-02-23\xa0 发布于拉勾网'

# resutl = re.match("",str)
# Log.info("-----")
# date = "1天前"
# date = "09:04"
# date = "2018-02-23"
# date = ""
# dateTime = ""
# if "天" in date:
#     match_result = re.match("(\d+)", date)
#     days = lambda: int(match_result.group(1)) if match_result else 1
#     dateTime = datetime.date.today() - datetime.timedelta(days=days())
#     # dateTime = time.strptime(dateTime.strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
#     dateTime = int(time.mktime(dateTime.timetuple()))
# elif ":" in date:
#     dateTime = int(time.mktime(time.strptime((datetime.date.today().strftime("%Y-%m-%d ") + date), "%Y-%m-%d %H:%M")))
# elif "-" in date:
#     dateTime = time.mktime(time.strptime(date,"%Y-%m-%d"))
# else:
#     dateTime = int(time.time())
# print(dateTime)

location = ['上海', '普陀区', '长寿路', '查看地图']

location = list(filter(lambda y: "地图" not in y, location))
print(location)

