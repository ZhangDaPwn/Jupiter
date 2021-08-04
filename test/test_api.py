#!/usr/bin/evn python
# -*- coding: utf-8 -*-
# @Time     : 2021/7/27 9:59
# @Author   : dapwn
# @File     : test_api.py
# @Software : PyCharm
import json

import requests

url = 'http://localhost:9595/track/'
headers = {
    'content-type': "application/json"
}
data = {
    'platform': '17track',
    'nums': [
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
    ],
    'description': 'test'
}

resp = requests.post(url, data=json.dumps(data))
print(resp)
print(resp.text)
