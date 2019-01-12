#!/usr/bin/python

from scapy.all import *
import os
import sys
import signal

from collectorClass import Collector

programName = "collector"
global shutdown_flag
shutdown_flag = 0


def terminate_process(signal_number, frame):
    global shutdown_flag
    shutdown_flag = 1
    print('(SIGTERM) terminating the process')


def main():
    signal.signal(signal.SIGINT, terminate_process)
    print("starting " + programName + " with PID: " + str(os.getpid()))
    collector = Collector("/home/newheres/datacom/802dot11/src/collectorConfig.json")
    collector.initialize()
    while not shutdown_flag:
        collector.start()
        collector.write_pcap_in_file()
        print("writing file: " + collector.get_output_file())
        collector.update_output_file()


main()


