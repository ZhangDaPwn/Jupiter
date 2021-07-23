#!/usr/bin/evn python
# -*- coding: utf-8 -*-
# @Time     : 2021/7/23 10:33
# @Author   : dapwn
# @File     : common_helper.py
# @Software : PyCharm
import time
import random
from datetime import datetime


class CommonHelper(object):
    def __init__(self):
        pass

    # 日期格式：2021-04-08 18:23:00
    def timestamp_to_utc_time(self, timestamp: int) -> str:
        utc_time = 0
        try:
            if timestamp != 0:
                timestamp = int(str(timestamp)[:10])
                utc_time = datetime.utcfromtimestamp(timestamp)
                # local_time = utc_time + timedelta(hours=8)
                utc_time = datetime.strftime(utc_time, "%Y-%m-%d %H:%M:%S")
        except:
            pass
        finally:
            return utc_time

    # 日期格式：2021-04-08 18:23:00
    def timestamp_to_local_time(self, timestamp: int) -> str:
        local_time = 0
        try:
            timestamp = int(str(timestamp)[:10])
            local_time = time.localtime(timestamp)
            local_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        except:
            pass
        finally:
            return local_time

    # 适用于pyppeteer生成的cookies转化
    def cookies_to_cookie(self, cookies: list) -> str:
        cookies = ['{}={}'.format(item['name'], item['value']) for item in cookies]
        cookie_str = ';'.join(cookies)
        return cookie_str

    # 自定义输入速度，防止反爬检测
    @property
    def input_time(self):
        return random.randint(100, 150)
