#!/usr/bin/python

from scapy.all import *
import os
import sys
import signal
import argparse
import time

from senderClass import Sender

programName = "sender"
global shutdown_flag
shutdown_flag = 0


def terminate_process(signal_number, frame):
    global shutdown_flag
    shutdown_flag = 1
    print('(SIGTERM) terminating the process')


def main():
    process_ready = 0
    if (sys.argv[1] != '-c') | (len(sys.argv) <= 2):
        print("use: " + programName + " -c [CONFIG_FILE]")
    signal.signal(signal.SIGINT, terminate_process)
    print("starting " + programName + " -c " + sys.argv[2] + " with PID: " + str(os.getpid()))
    cfg_file = sys.argv[2]
    sender_inst = Sender(cfg_file)
    while not shutdown_flag:
        try:
            if process_ready == 0:
                process_ready = sender_inst.initialize()
            print("sender type: " + sender_inst.conf['cfgFromFile']['type'])
            sender_inst.send(sender_inst.conf['cfgFromFile']['type'])
            # sender_inst.write_pcap_in_file()
            # sender_inst.update_output_file()
            print("watting 5 seconds for files")
            time.sleep(5)
        except ConnectionResetError as e1:
            print('[' + programName + ']' + ' Exception: process exit', e1)
            exit()
        except Exception as e2:
            print('[' + programName + ']' + ' Exception: waitting 5 seconds ..')
            time.sleep(5)


main()
