### 项目介绍

该项目为物流信息查询服务，整合市面上的主流物流查询平台的物流信息

### 目标网站

| 目标网站 | 网站地址 | 是否支持 |
| :----: | :----: | :----: |
| 17track | https://www.17track.net/en | 支持 |

### 安装依赖

`pip install -r requirements.txt`

### 启动命令

##### Linux：

`nohup python3 main.py`

##### Windows:

###### 后台运行

`start /min python3 main.py`

###### 前台运行

`python3 main.py`

### 服务API列表

| METHOD | API | 参数 | 说明 |
| :----: | :---: | :---: | :---: |
| POST | /track/ | {"platform": string,"nums": list,"description": string} | 物流信息查询接口 |

[测试链接](http://127.0.0.1:9595/docs)

[服务API查看](http://127.0.0.1:9595/redoc)
