#!/usr/bin/python

from scapy.all import *
import json
import datetime
from dataUtilsClass import dataUtils


class wifiCollector(dataUtils):

    def __init__(self, conf_file):
        self.conf = {
                'cfgFromFile': {
                    'interface': '',
                    'outputDir': '',
                    'outputFileMask': '',
                    'outputExt': '',
                    'size': 1,
                    "seqDig": 0
                    },
                'cfgFromProc': {
                    'configFile': conf_file,
                    'outputFile': '',
                    'readPackets': 0,
                    'writePackets': 0,
                    'seqNumber': 0,
                    'maxSeqNumber': 0,
                    'number_of_files': 0
                    }
                }
        self.__readPackets = 0
        self.__writePackets = 0
        self.__number_of_files = 0
        self.pkt = []
        self.class_name = "wifiCollectorClass"

    def start(self):
        sniff(count=self.conf['cfgFromFile']['size'], iface=self.conf['cfgFromFile']['interface'], \
                prn=self.packet_handler)

    def initialize(self):
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

    def get_next_sequence_number(self):
        if (self.conf['cfgFromProc']['seqNumber'] < self.conf['cfgFromProc']['maxSeqNumber']) & \
           (self.conf['cfgFromProc']['seqNumber'] >= 0):
            return self.conf['cfgFromProc']['seqNumber'] + 1
        else:
            if self.conf['cfgFromProc']['seqNumber'] == self.conf['cfgFromProc']['maxSeqNumber']:
                return 0

    def set_sequence_number(self, num):
        if num <= self.conf['cfgFromProc']['maxSeqNumber'] | self.conf['cfgFromProc']['seqNumber'] >= 0:
            self.conf['cfgFromProc']['seqNumber'] = num
        else:
            print("ERROR. numero de secuencia invalido")

    def update_output_file(self):
        now = datetime.datetime.now()
        self.conf['cfgFromProc']['outputFile'] = self.conf['cfgFromFile']['outputDir'] + \
                                                 self.conf['cfgFromFile']['outputFileMask'] + \
                                                 now.strftime("%Y%m%d_%H%M%S") + "_" + \
                                                 format(self.conf['cfgFromProc']['seqNumber'], "05d") + \
                                                 "." + self.conf['cfgFromFile']['outputExt']

        self.set_sequence_number(self.get_next_sequence_number())

    def packet_handler(self, pkt):
        # me quedo solo con los paquetes con layer 802.11
        if pkt.haslayer(Dot11):
            self.pkt.append(pkt)

    def write_pcap_in_file(self):
        wrpcap(self.conf['cfgFromProc']['outputFile'], self.pkt)
        self.__number_of_files = self.__number_of_files + 1
        self.pkt = []

