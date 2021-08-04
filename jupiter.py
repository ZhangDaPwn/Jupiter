#!/usr/bin/evn python
# -*- coding: utf-8 -*-
# @Time     : 2021/7/23 11:55
# @Author   : dapwn
# @File     : saturn.py
# @Software : PyCharm
import time
import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel, Field

from handler.log_handler import LogHandler
from fetcher.track17 import Track17
from settings import BANNER, slogan, PORT

app = FastAPI()
name = 'jupiter'
log = LogHandler(name=name)


class Tracker(BaseModel):
    platform: str = Field(..., description="The platform is track platform")
    # nums: str = Field(..., description="The muns must be separated by ','")
    nums: list = Field(..., description="The muns must be list array")
    description: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Welcome to use jupiter!"}


@app.post("/track/")
async def track(item: Tracker):
    log.info("本次抓取的入参为：", str(item))
    if item.platform == '17track':
        nums = item.nums
        data = await Track17(nums=nums).main()
    else:
        data = {'message': 'The parameters are incorrect. Please check it!'}
    return data


if __name__ == '__main__':
    print(BANNER)
    print(slogan, '\n')
    uvicorn.run(
        app='jupiter:app',
        host='0.0.0.0',
        port=PORT,
        reload=True,
        debug=True
    )
