#!/usr/bin/python

import os
import sys
import signal
from receiverClass import Receiver

programName = "receiver"
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
    receiver = Receiver(cfg_file)
    try:
        receiver.initialize()
    except KeyError:
        print('[' + programName + ']' + ' Exception: process exit')
        exit()
    while not shutdown_flag:
        try:
            receiver.start()
            # receiver.write_pcap_in_file()
            #print("writing file: " + receiver.conf['cfgFromProc']['outputFile'])
            receiver.update_output_file()
        except Exception as e1:
            print('[' + programName + ']' + ' Exception: process exit', e1)
            # maybe check if the was close
            exit()


main()

