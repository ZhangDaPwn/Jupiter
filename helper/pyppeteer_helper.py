#!/usr/bin/evn python
# -*- coding: utf-8 -*-
# @Time     : 2021/7/23 11:13
# @Author   : dapwn
# @File     : pyppeteer_helper.py
# @Software : PyCharm
"""
-------------------------------------------------
   Description :  pyppeteer助手
   date：          2021/7/23
-------------------------------------------------

-------------------------------------------------
"""
__author__ = 'dapwn'

import random
from pyppeteer import launch

from handler.log_handler import LogHandler
from utils import ua
from settings import PROXY_USERNAME, PROXY_PASSWORD


class PyppeteerHelper(object):
    def __init__(self,
                 use_proxy: bool = False,
                 is_tunnel: bool = False,
                 headless: bool = True,
                 user_agent: str = random.choice(ua.ua_track),
                 proxy: str = None):
        self.name = 'PyppeteerHelper'
        self.log = LogHandler(self.name)
        self.use_proxy = use_proxy
        self.is_tunnel = is_tunnel
        self.headless = headless
        self.user_agent = user_agent
        self.proxy = proxy

    @property
    async def browser_init(self):
        if self.use_proxy:
            if self.is_tunnel:
                browser = await launch({
                    'headless': self.headless,
                    # 'executablePath': '',
                    'args': [
                        '--user-agent={}'.format(self.user_agent),
                        '--disable-extensions',
                        '--disable-bundled-ppapi-flash',
                        '--mute-audio',
                        '--no-sandbox',  # 沙盒模式 --no-sandbox 在 docker 里使用时需要加入的参数，不然会报错
                        '--disable-setuid-sandbox',
                        '--disable-gpu',
                        '--disable-xss-auditor',
                    ],
                    'dumpio': True,  # 解决浏览器多开卡死
                })
                page = await browser.newPage()
                # 针对隧道代理，进行账密验证
                await page.authenticate({'username': PROXY_USERNAME, 'password': PROXY_PASSWORD})
                await page.evaluateOnNewDocument(
                    'function(){Object.defineProperty(navigator, "webdriver", {get: () => undefined})}')
            else:
                proxy = '47.105.111.124:15525'
                browser = await launch({
                    'headless': self.headless,
                    # 'executablePath': '',
                    'args': [
                        '--user-agent={}'.format(self.user_agent),
                        '--proxy-server={}'.format(proxy),  # 无账号密码代理 如：47.105.111.124:15525
                        '--disable-extensions',
                        '--disable-bundled-ppapi-flash',
                        '--mute-audio',
                        '--no-sandbox',  # 沙盒模式 --no-sandbox 在 docker 里使用时需要加入的参数，不然会报错
                        '--disable-setuid-sandbox',
                        '--disable-gpu',
                        '--disable-xss-auditor',
                    ],
                    'dumpio': True,  # 解决浏览器多开卡死
                })
                page = await browser.newPage()
                await page.evaluateOnNewDocument(
                    'function(){Object.defineProperty(navigator, "webdriver", {get: () => undefined})}')
        else:
            browser = await launch({
                'headless': self.headless,
                'args': [
                    '--user-agent={}'.format(self.user_agent),
                    '--disable-extensions',
                    '--disable-bundled-ppapi-flash',
                    '--mute-audio',
                    '--no-sandbox',  # 取消沙盒模式 沙盒模式下权限太小
                    # '--start-maximized',  # 窗口最大化模式
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                    '--disable-xss-auditor',
                ],
                'dumpio': True,  # 解决浏览器多开卡死
            })
            page = await browser.newPage()
            await page.evaluateOnNewDocument(
                'function(){Object.defineProperty(navigator, "webdriver", {get: () => undefined})}')
        return browser, page
