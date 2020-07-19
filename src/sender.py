#!/usr/bin/python

from scapy.all import *
import os
import sys
import argparse
import time
from senderClass import Sender

programName = "sender"
global wait_time
wait_time = 5


def main():
    process_ready = 0
    if (sys.argv[1] != '-c') | (len(sys.argv) <= 2):
        print("use: " + programName + " -c [CONFIG_FILE]")

    print("starting " + programName + " -c " + sys.argv[2] + " with PID: " + str(os.getpid()))
    cfg_file = sys.argv[2]
    sender_inst = Sender(cfg_file)
    while not sender_inst.received_term_sig():
        print("sender recived_term_sig: ", sender_inst.received_term_sig())
        try:
            if process_ready == 0:
                process_ready = sender_inst.initialize()
            print("sender type: " + sender_inst.conf['cfgFromFile']['type'])
            sender_inst.send(sender_inst.conf['cfgFromFile']['type'])
            # sender_inst.write_pcap_in_file()
            # sender_inst.update_output_file()
            print("waiting " + wait_time + " seconds for files")
            time.sleep(wait_time)
        except socket.error as ex:
            print('[' + programName + ']' + " can not connect to server: " + str(ex))
            time.sleep(wait_time)
        except ConnectionResetError as e1:
            print('[' + programName + ']' + ' Exception: process exit', str(e1))
            time.sleep(wait_time)
            exit()
        except Exception as e2:
            print('[' + programName + ']' + ' Exception: ', str(e2))
            time.sleep(wait_time)


main()
