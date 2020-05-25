#!/usr/bin/env bash

my_proc=`ps aux | grep -E "sudo python wifiCollector.py -c wifiCollectorConfig.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" == "" ]
then
    echo "wifiCollector is not running"
else
    echo "wifiCollector is running with pid: $my_pid"
fi
exit 0