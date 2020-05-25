#!/usr/bin/env bash

myInterface=`iw dev | grep mon0 | awk '{print $2}'`
if [ "$myInterface" != "mon0" ]
then
    echo "no se encontro interface: mon0"
    exit 1
fi
type=`sudo iw dev mon0 info | grep type | awk '{print $2}'`
if [ "$type" != "monitor" ]
then
    echo "no se encontro interface modo monitor"
    exit 1
fi
# run wifi collector first process in the batch chain
my_proc=`ps aux | grep -E "sudo python wifiCollector.py -c wifiCollectorConfig.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" == "" ]
then
    sudo python wifiCollector.py -c wifiCollectorConfig.json > /dev/null 2>&1 &
else
    echo "wifiCollector is already running with pid: $my_pid"
fi

# run sender second process in the batch chain






