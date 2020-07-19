#!/usr/bin/python
# Este programa esta creado para ser ejecutado con python 3.6

from scapy.all import *
import json
import signal
import datetime
import pdb; pdb.set_trace()
from dataUtilsClass import dataUtils

class wifiCollector(dataUtils):

    def __init__(self, conf_file):
        self.conf = {
                'cfgFromFile': {
                    'interface': '',
                    'outputDir': '',
                    'outputFileMask': '',
                    'outputExt': '',
                    'tmpOutputExt': '',
                    'size': 1,
                    "seqDig": 0
                    },
                'cfgFromProc': {
                    'configFile': conf_file,
                    'outputFile': '',
                    'finalOutputFile': '',
                    'readPackets': 0,
                    'writePackets': 0,
                    'seqNumber': 0,
                    'maxSeqNumber': 0,
                    'number_of_files_w': 0
                    }
                }
        self.pkt = []
        self.class_name = "wifiCollectorClass"
        self.shutdown_flag = False

    def start(self):
        try:
            sniff(count=self.conf['cfgFromFile']['size'], iface=self.conf['cfgFromFile']['interface'],
                  prn=self.packet_handler)
        except (PermissionError, OSError) as e1:
            print('[' + self.class_name + ']' + ' Exception: ', e1)
            raise Exception("Error when try to pull data wifi")
        print("writing file: " + self.conf['cfgFromProc']['finalOutputFile'])
        self.write_dot11_in_pcap()
        self.pkt = []
        self.update_output_file()

    def scan(self):
        try:
            sniff(count=1, iface=self.conf['cfgFromFile']['interface'],
                  prn=self.packet_handler)
        except (PermissionError, OSError) as e1:
            print('[' + self.class_name + ']' + ' Exception: ', e1)
            raise Exception("Error when try to pull data wifi")
        print(self.pkt)
        self.pkt = []

    def initialize(self):
        signal.signal(signal.SIGINT, self.terminate_process)
        with open(self.conf['cfgFromProc']['configFile']) as json_file:
            text = json_file.read()
            json_data = json.loads(text)
            # necesito setear todos estos parametros para que se ejecute
            # el proceso. Los datos son obtenidos del archivo de configuracion
            for key in self.conf['cfgFromFile'].keys():
                try:
                    self.conf['cfgFromFile'][key] = self.get_value_from_json(json_data, key)
                except KeyError as e1:
                    print('[' + self.class_name + ']' + ' Exception: ', e1)
                    raise KeyError("Error reading necessary keys to execute the process")
            number_of_digits = self.conf['cfgFromFile']['seqDig']
            self.conf['cfgFromProc']['maxSeqNumber'] = 10 ** int(number_of_digits) - 1
            self.conf['cfgFromProc']['seqNumber'] = 0
            self.update_output_file()

    def terminate_process(self, signum, frame):
        self.shutdown_flag = True
        print('(SIGTERM) terminating the process')

    def received_term_sig(self):
        return self.shutdown_flag

    def packet_handler(self, pkt):
        # me quedo solo con los paquetes con layer 802.11
        # no funciona Dot11
        # https://github.com/secdev/scapy/issues/1590
        # utilizo beacon porque son los que me interesan para ver las redes
        if pkt.haslayer(Dot11Beacon):
            self.pkt.append(pkt)

