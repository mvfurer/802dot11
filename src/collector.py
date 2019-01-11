#!/usr/bin/python

from scapy.all import *

import sys

from collectorClass import Collector

programName = "collector"

def main():
    print("starting " + programName + " main ...")
    collector = Collector("/home/newheres/datacom/802dot11/agent/config/config.json")
    collector.initialize()
    conf.iface = collector.get_interface()
    for i in range(0, collector.get_size()):
        sniff(count=1, prn=packet_handler)
    print(collector.get_config_file())


main()


