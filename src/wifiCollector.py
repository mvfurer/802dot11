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
from wifiCollectorClass import wifiCollector

programName = "wifiCollector"


def main():
    if (sys.argv[1] != '-c') | (len(sys.argv) <= 2):
        print("use: " + programName + " -c [CONFIG_FILE]")
    print("starting " + programName + " with PID: " + str(os.getpid()))
    cfg_file = sys.argv[2]
    collector = wifiCollector(cfg_file)
    try:
        collector.initialize()
    except KeyError:
        print('[' + programName + ']' + ' Exception: process exit')
        exit()
    while not collector.received_term_sig():
        try:
            collector.start()
        except Exception as e1:
            print('[' + programName + ']' + ' Exception: process exit', str(e1))
            exit()


main()


