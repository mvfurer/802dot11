#!/usr/bin/env bash

my_proc=`ps aux | grep -E "sudo python wifiCollector.py -c wifiCollectorConfig.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" != "" ]
then
    sudo kill $my_pid
fi
exit 0