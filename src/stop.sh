#!/usr/bin/env bash
# Detiene los procesos en ejecucion

#stop sender db
my_proc=`ps aux | grep -E "python sender.py -c senderConfig_db.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" != "" ]
then
    sudo kill $my_pid
fi

#stop receiver
my_proc=`ps aux | grep -E "python receiver.py -c receiverConfig.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" != "" ]
then
    sudo kill $my_pid
fi

#stop sender
my_proc=`ps aux | grep -E "python sender.py -c senderConfig.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" != "" ]
then
    sudo kill $my_pid
fi

#stop wificollector
my_proc=`ps aux | grep -E "sudo python wifiCollector.py -c wifiCollectorConfig.json" | grep -v grep`
my_pid=`echo $my_proc | awk '{print $2}'`
if [ "$my_pid" != "" ]
then
    sudo kill $my_pid
fi
exit 0