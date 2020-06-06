#!/usr/bin/python
# Este programa esta creado para ser ejecutado con python 3.6
# debe ejecutarse con usuario root
# debe configurarse la placa de wifi en modo monitor:
# ej:
# iw phy phy1 interface add mon0 type monitor
# ifconfig mon0 up
# iw dev mon0 set freq 2412   (opcional)
# captura los paquetes beacon de 802.11

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
    # TODO: rename all tmp files to pcap
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
        try:
            collector.start()
            collector.update_output_file()
        except Exception as e1:
            print('[' + programName + ']' + ' Exception: process exit', e1)
            exit()


main()


