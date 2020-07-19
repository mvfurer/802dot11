#!/usr/bin/python

import os
import sys
from receiverClass import Receiver

programName = "receiver"

def main():
    if (sys.argv[1] != '-c') | (len(sys.argv) <= 2):
        print("use: " + programName + " -c [CONFIG_FILE]")
    print("starting " + programName + " with PID: " + str(os.getpid()))
    cfg_file = sys.argv[2]
    receiver = Receiver(cfg_file)
    try:
        receiver.initialize()
    except KeyError:
        print('[' + programName + ']' + ' Exception: process exit')
        exit()
    while not receiver.received_term_sig():
        try:
            receiver.start()
            # receiver.write_pcap_in_file()
            #print("writing file: " + receiver.conf['cfgFromProc']['outputFile'])
        except Exception as e1:
            print('[' + programName + ']' + ' Exception: process exit', str(e1))
            # maybe check if the was close
            exit()


main()

