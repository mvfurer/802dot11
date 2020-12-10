#!/usr/bin/env bash
# this script starts all the processes

#checking monitor interface
myInterface=`iw dev | grep mon0 | awk '{print $2}'`
if [ "$myInterface" != "mon0" ]
then
    echo "Monitor interface: mon0  -  was not found"
    exit 1
fi
type=`sudo iw dev mon0 info | grep type | awk '{print $2}'`
if [ "$type" != "monitor" ]
then
    echo "no se encontro interface modo monitor"
    exit 1
fi

# run sender to db
my_proc=`ps aux | grep -E "python sender.py -c senderConfig_db.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" == "" ]
then
    echo "sender db process is starting"
    python sender.py -c senderConfig_db.json > /dev/null 2>&1 &
else
    echo "sender db process is already running with pid: $my_pid"
fi

# run receiver
my_proc=`ps aux | grep -E "python receiver.py -c receiverConfig.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" == "" ]
then
    echo "receiver server process is starting"
    python receiver.py -c receiverConfig.json > /dev/null 2>&1 &
else
    echo "receiver server process is already running with pid: $my_pid"
fi

# sleep 5

# run sender to server
my_proc=`ps aux | grep -E "python sender.py -c senderConfig.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" == "" ]
then
    echo "sender client process is starting"
    python sender.py -c senderConfig.json > /dev/null 2>&1 &
else
    echo "sender client process is already running with pid: $my_pid"
fi

sleep 5

# run wifi collector
my_proc=`ps aux | grep -E "sudo python wifiCollector.py -c wifiCollectorConfig.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" == "" ]
then
    echo "wifi collector process is starting"
    sudo python wifiCollector.py -c wifiCollectorConfig.json > /dev/null 2>&1 &
else
    echo "wifiCollector process is already running with pid: $my_pid"
fi
