#!/bin/sh
source /etc/profile
echo "stop server..."
cd /root/jupiter
pidlist=`ps -ef |grep python3 | awk '{print $2}'`
kill -9 $pidlist

echo "delete temp file success..."
nohup python3 main.py &
echo "start server..."
sleep 15