#!/usr/bin/env bash
# verifica el PID de los procesos

my_proc=`ps aux | grep -E "python sender.py -c senderConfig_db.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" == "" ]
then
    echo "sender db process is not running"
else
    echo "sender db process is running with pid: $my_pid"
fi

my_proc=`ps aux | grep -E "python receiver.py -c receiverConfig.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" == "" ]
then
    echo "receiver server process is not running"
else
    echo "receiver server process is running with pid: $my_pid"
fi

my_proc=`ps aux | grep -E "python sender.py -c senderConfig.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" == "" ]
then
    echo "sender client process is not running"
else
    echo "sender client process is running with pid: $my_pid"
fi

my_proc=`ps aux | grep -E "sudo python wifiCollector.py -c wifiCollectorConfig.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" == "" ]
then
    echo "wifiCollector process is not running"
else
    echo "wifiCollector process is running with pid: $my_pid"
fi
exit 0