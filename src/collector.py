#!/usr/bin/python

from scapy.all import *

import sys

from collectorClass import Collector

programName = "collector"


def main():
    print("starting " + programName + " main ...")
    collector = Collector("/home/newheres/datacom/802dot11/src/collectorConfig.json")
    collector.initialize()
    while collector.get_number_of_files() < 5:
        collector.start()
        collector.write_pcap_in_file()
        print("writing file: " + collector.get_output_file())
        collector.update_output_file()
        print("updated file to: " + collector.get_output_file())


main()


