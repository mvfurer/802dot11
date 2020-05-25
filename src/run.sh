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

sudo python wifiCollector.py -c wifiCollectorConfig.json

