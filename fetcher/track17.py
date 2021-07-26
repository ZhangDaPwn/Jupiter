#!/usr/bin/evn python
# -*- coding: utf-8 -*-
# @Time     : 2021/7/12 16:55
# @Author   : dapwn
# @File     : track17.py
# @Software : PyCharm
import os
import random
import asyncio
import time
import json
import nest_asyncio
from urllib.parse import urljoin
from utils.ua import ua_track
from utils.chaojiying import VerifyHandler
from handler.log_handler import LogHandler
from helper.common_helper import CommonHelper
from helper.http_helper import HttpHelper
from helper.pyppeteer_helper import PyppeteerHelper
from settings import *

nest_asyncio.apply()  # asyncio默认不允许嵌套时间循环，加上这个方法，声明允许使用


class Track17(object):
    def __init__(self, nums: list):
        self.headless = False  # 是否使用无头浏览器
        self.use_proxy = False  # 是否使用代理
        self.is_tunnel = False  # 是否为隧道代理
        self.name = 'Track17'
        self.ua = random.choice(ua_track)
        print("本次请求的User-Agent:", self.ua)
        self.log = LogHandler(self.name)
        self.ch = CommonHelper()
        self.hh = HttpHelper()
        self.ph = PyppeteerHelper(user_agent=self.ua)
        self.num_list = nums
        self.num_str = ','.join(nums)
        # self.num_list = list(filter(lambda s: s and s.strip(), nums.split(',')))
        self.origin = 'https://www.17track.net'
        self.url_0 = 'https://t.17track.net/en#nums={}'.format(self.num_str)  # 获取cookie地址
        self.url_1 = 'https://t.17track.net/restapi/track'  # 获取物流数据地址
        self.expire_time = 600  # cookie等数据存活时长
        self.status_code = {
            '0': {'en': 'Not Found', 'zh': '查询不到'},
            '10': {'en': 'In Transit', 'zh': '运输途中'},
            '30': {'en': 'Pick Up', 'zh': '到达待取'},
            '35': {'en': 'Undelivered', 'zh': '投递失败'},
            '40': {'en': 'Delivered', 'zh': '签收成功'},
            '50': {'en': 'Alert', 'zh': '可能异常'},
            '20': {'en': 'Expired', 'zh': '运输过久'},
        }

    # 暂时未用到，后面做异常统计
    def error_condition(self):
        errors = {
            'error_0': {"ret": -8, "msg": "abN", "dat": []},  # 未获取到数据，返回类型一
            'error_1': {"ret": -7, "msg": "numNon", "dat": []}  # 浏览器版本过低
        }
        return errors

    async def verify(self, page):
        try:
            # 获取验证码图片链接
            verify_img = await page.xpath('//img[@id="var-img"]')  # xpath 获取到的数据为一个list
            if verify_img:
                print("出现验证码，进行打码验证操作...")

                CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
                ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
                PIC_PATH = os.path.join(ROOT_PATH, 'pic')
                if not os.path.exists(PIC_PATH):
                    try:
                        os.mkdir(PIC_PATH)
                    except FileExistsError:
                        pass

                img_src = await (await verify_img[0].getProperty('src')).jsonValue()
                print("验证码图片地址:", img_src)
                img_url = urljoin(self.origin, str(img_src))
                img_path = PIC_PATH + '/17track_{}.jpg'.format(str(int(time.time())))
                self.hh.get(url=img_url, header={'User-Agent': self.ua}).download(img_path)
                v_result = VerifyHandler().main(img_path=img_path, code_type=CJY_CODE_ID)
                print("验证码识别结果：", v_result)
                if v_result['err_str'] == 'OK':
                    code = v_result['pic_str']
                    # 获取验证码输入框，输入验证码
                    await page.type('#ver-code-input', code, {'delay': self.ch.input_time})
                    await asyncio.sleep(1)
                    # 填写完验证码，点击confirm按钮
                    confirm_button = await page.xpath(
                        '//button[@class="btn btn-block btn-primary btn-submit waves-effect"]')
                    await confirm_button[0].click()
                    await asyncio.sleep(5)
        except:
            self.log.info('本次爬取未出现验证码')

    async def get_headers(self):
        headers = {
            "Host": "t.17track.net",
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua-mobile": "?0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Length": "{}".format(len(self.num_list) * 40),
            "Origin": "https://t.17track.net",
            "Referer": "https://t.17track.net/en",
            "Cookie": "",
            "User-Agent": self.ua,
        }
        browser, page = await self.ph.browser_init  # 获取初始化后的page
        try:
            await page.goto(self.url_0)
            time.sleep(3)
            # 过验证码操作
            try:
                await self.verify(page)
            except:
                pass

            cookies = await page.cookies()

            header = {
                'Cookie': self.ch.cookies_to_cookie(cookies)
            }
            headers.update(header)

        except Exception as e:
            self.log.error(e)
        finally:
            await browser.close()
            return headers

    async def parse(self, data: dict) -> list:
        track_data = []
        try:
            ret = data['ret']  # 本次查询状态码： 1
            msg = data['msg']  # 本次查询返回信息： Ok
            if ret == 1 and msg == 'Ok':
                dat = data['dat']
                for item in dat:
                    logistics = {}
                    logistics['track_number'] = item['no']  # 订单号： SF6043171924470
                    logistics['query_status'] = ret  # 查询状态: 1:成功 0：失败
                    logistics['query_response'] = msg  # 接口返回信息: Ok:成功 error：失败
                    logistics['status'] = self.status_code[str(item['track']['e'])]['en']  # 物流状态
                    logistics['status_zh'] = self.status_code[str(item['track']['e'])]['zh']
                    # logistics['delay'] = item['delay']  # 可能是物流延迟状态：0
                    track = {}
                    track['z0'] = item['track']['z0']
                    track['z1'] = item['track']['z1']
                    track['z2'] = item['track']['z2']
                    track['z9'] = item['track']['z9']
                    zex = item['track']['zex']
                    zex['dt'] = self.ch.timestamp_to_utc_time(zex['dt'])
                    zex['dtS'] = self.ch.timestamp_to_utc_time(zex['dtS'])
                    zex['dtP'] = self.ch.timestamp_to_utc_time(zex['dtP'])
                    zex['dtD'] = self.ch.timestamp_to_utc_time(zex['dtD'])
                    zex['dtL'] = self.ch.timestamp_to_utc_time(zex['dtL'])
                    track['zex'] = zex
                    logistics['track'] = track
                    track_data.append(logistics)
            else:
                print("本次物流查询失败！")
        except Exception as e:
            self.log.error(e)
        finally:
            return track_data

    async def main(self):
        info = {}
        try:
            headers = await self.get_headers()
            data = {"data": [{"num": num, "fc": 0, "sc": 0} for num in self.num_list],
                    "guid": "",
                    "timeZoneOffset": -480}
            data = self.hh.post(url=self.url_1, header=headers, data=json.dumps(data)).json
            info = await self.parse(data=data)
            if not len(info[0]['track_number']):
                self.log.info("本次未获取到数据，请检查是否与UA或者PROXY有关！UA:{} PROXY:{}".format(self.ua, ''))
        except Exception as e:
            self.log.error(e)
        finally:
            return info


if __name__ == '__main__':
    start_time = time.time()
    # 查询不到
    num0 = [
        'SF6043165115610',
        'SF6043189141136',
        'SF6043180120692',
        'SF6043183429845',
        'SF6043167499860',
    ]
    # 成功签收
    num1 = [
        'SF6043175416258',
        'SF6043175001100',
        'SF6043175006554',
        'SF6043175027633',
        'SF6043179817219',
        'SF6043175675715',
        'SF6043175692391',
        'SF6043166165373',
        'SF6043175667836',
        'SF6043195392126',
    ]
    # 到达待取
    num2 = [
        'SF6043185656483',
        'SF6043182090162',
        'SF6043179465266',
        'SF6043175700955',
        'SF6043167600037',
    ]
    # 可能异常
    num3 = [
        'SF6043165135871',
        'SF6043193439428',
        'LY802191446CN',
        'LY802189558CN',
        'LZ911479180CN',
    ]
    # 投递失败
    num4 = [
        'SF6043174647755',
        'SF6043187569794',
        'SF6043178701441',
        'SF6043175012822',
        'SF6043178718490',
    ]
    # 运输途中
    num5 = [
        'SF6043192688506',
        'SF6043194561994',
        'SF6043193440096',
        'SF6043192788879',
        'SF6043192687026',
    ]
    # 运输过久
    num6 = [
        'SF6043144806426',
        'SF6043146515494',
        'SF6043144742400',
        'SF6043138868993',
        'SF6043144823289',
    ]

    nums = num0 + num1 + num2 + num3 + num4 + num5 + num6
    track = Track17(nums=nums)
    result = track.main()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("耗时：", time.time() - start_time)
