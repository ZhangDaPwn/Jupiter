#!/bin/sh
source /etc/profile

echo "stop server..."
cd /root/Jupiter
pidlist=`ps -ef |grep jupiter.py | awk '{print $2}'`
kill -9 $pidlist

pidlist=`ps -ef |grep multiprocessing | awk '{print $2}'`
kill -9 $pidlist

echo "delete temp file success..."
nohup python3 jupiter.py &
echo "start server..."
sleep 15
