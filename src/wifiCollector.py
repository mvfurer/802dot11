#!/usr/bin/python

from scapy.all import *
import os
import sys
import signal
from wifiCollectorClass import wifiCollector

programName = "wifiCollector"
global shutdown_flag
shutdown_flag = 0


def terminate_process(signal_number, frame):
    global shutdown_flag
    shutdown_flag = 1
    print('(SIGTERM) terminating the process')


def main():
    if (sys.argv[1] != '-c') | (len(sys.argv) <= 2):
        print("use: " + programName + " -c [CONFIG_FILE]")
    signal.signal(signal.SIGINT, terminate_process)
    print("starting " + programName + " with PID: " + str(os.getpid()))
    cfg_file = sys.argv[2]
    collector = wifiCollector(cfg_file)
    try:
        collector.initialize()
    except KeyError:
        print('[' + programName + ']' + ' Exception: process exit')
        exit()
    while not shutdown_flag:
        collector.start()
        collector.write_pcap_in_file()
        print("writing file: " + collector.conf['cfgFromProc']['outputFile'])
        collector.update_output_file()


main()


