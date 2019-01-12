#!/usr/bin/python

from scapy.all import *
import json
import datetime


class Collector:

    def __init__(self, conf_file):
        self.__configFile = conf_file
        self.__interface = ""
        self.__outputDir = ""
        self.__outputFileMask = ""
        self.__outputExt = ""
        self.__outputFile = ""
        self.__readPackets = 0
        self.__writePackets = 0
        self.__size = 1
        self.__seqNumber = 0
        self.__maxSeqNumber = 0
        self.__number_of_files = 0
        self.pkt = []
        super(Collector, self).__init__()

    def start(self):
        sniff(count=self.get_size(), iface=self.get_interface(), prn=self.packet_handler)

    def initialize(self):
        config_file = self.__configFile
        with open(config_file) as json_file:
            text = json_file.read()
            json_data = json.loads(text)
            # necesito setear todos estos parametros para que se ejecute
            # el proceso.

            if 'interface' not in json_data:
                raise KeyError("no se encontro key: interface")
            else:
                self.__interface = json_data['interface']

            if 'outputDir' not in json_data:
                raise KeyError("no se encontro key: outputDir")
            else:
                self.__outputDir = json_data['outputDir']

            if 'outputFileMask' not in json_data:
                raise KeyError("no se encontro key: outputFileMask")
            else:
                self.__outputFileMask = json_data['outputFileMask']

            if 'outputExt' not in json_data:
                raise KeyError("no se encontro key: outputExt")
            else:
                self.__outputExt = json_data['outputExt']

            if 'size' not in json_data:
                raise KeyError("no se encontro key: size")
            else:
                self.__size = json_data['size']

            if 'seqDig' not in json_data:
                raise KeyError("no se encontro key: seqDig")
            else:
                number_of_digits = json_data['seqDig']
                self.__seqNumber = 0
                self.__maxSeqNumber = 10**int(number_of_digits)-1
            self.update_output_file()

    def get_config_file(self):
        return self.__configFile

    def get_interface(self):
        return self.__interface

    def get_output_dir(self):
        return self.__outputDir

    def get_output_file_mask(self):
        return self.__outputFileMask

    def get_output_file_ext(self):
        return self.__outputExt

    def get_output_file(self):
        return self.__outputFile

    def get_read_packets(self):
        return self.__readPackets

    def get_write_packets(self):
        return self.__writePackets

    def get_size(self):
        return self.__size

    def get_sequence_number(self):
        return self.__seqNumber

    def get_max_sequence_number(self):
        return self.__maxSeqNumber

    def get_number_of_files(self):
        return self.__number_of_files

    def get_next_sequence_number(self):
        if (self.__seqNumber < self.__maxSeqNumber) & (self.__seqNumber >= 0):
            return self.__seqNumber + 1
        else:
            if self.__seqNumber == self.__maxSeqNumber:
                return 0

    def set_sequence_number(self, num):
        if num <= self.__maxSeqNumber | self.__seqNumber >= 0:
            self.__seqNumber = num
        else:
            print("ERROR. numero de secuencia invalido")

    def update_output_file(self):
        now = datetime.datetime.now()
        self.__outputFile = self.get_output_dir() + self.get_output_file_mask() + \
                            now.strftime("%Y%m%d_%H%M%S") + "_" + format(self.get_sequence_number(), "05d")
        self.set_sequence_number(self.get_next_sequence_number())

    def packet_handler(self, pkt):
        # me quedo solo con los paquetes con layer 802.11
        if pkt.haslayer(Dot11):
            self.pkt.append(pkt)

    def write_pcap_in_file(self):
        wrpcap(self.__outputFile, self.pkt)
        self.__number_of_files = self.__number_of_files + 1
        self.pkt = []

