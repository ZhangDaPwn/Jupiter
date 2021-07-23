#!/usr/bin/evn python
# -*- coding: utf-8 -*-
# @Time     : 2021/7/23 11:55
# @Author   : dapwn
# @File     : main.py
# @Software : PyCharm
import time
import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel, Field

from fetcher.track17 import Track17
from settings import BANNER, slogan, PORT

app = FastAPI()


class Tracker(BaseModel):
    platform: str = Field(..., description="The platform is track platform")
    nums: str = Field(..., description="The muns must be separated by ','")
    description: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Welcome to use jupiter!"}


@app.post("/track/")
async def track(item: Tracker):
    start_time = time.time()
    if item.platform == '17track':
        nums = item.nums
        print("本次请求订单号为：", nums)
        data = await Track17(nums=nums).main()
    else:
        data = {'message': 'The parameters are incorrect. Please check it!'}
    print("订单：{} 耗时：{}".format(item.nums, time.time() - start_time))
    return data


if __name__ == '__main__':
    print(BANNER)
    print(slogan)
    uvicorn.run(
        app='main:app',
        host='localhost',
        port=PORT,
        reload=True,
        debug=True
    )
