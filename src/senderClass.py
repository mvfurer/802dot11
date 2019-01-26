#!/usr/bin/env python

"""
clase sender que envia los paquetes guardados en pcap file
basado en el programa

"""
from collectorClass import Collector
from scapy.all import *
import socket
import sys
import argparse
import json
import glob
import datetime


class Sender(Collector):

    def __init__(self, conf_file):
        self.__conf = conf_file
        self.__number_of_files_w = 0
        self.__number_of_files_r = 0
        super().__init__(self.__conf)

    def initialize(self):
        config_file = self.get_config_file()
        with open(config_file) as json_file:
            text = json_file.read()
            json_data = json.loads(text)
            """
            necesito setear todos estos parametros para que se ejecute
            el proceso.
            """
            self.__number_of_files_w = 0
            self.__number_of_files_r = 0
            self.pkt = []

            if 'host' not in json_data:
                raise KeyError("no se encontro key: host")
            else:
                self.host = json_data['host']

            if 'port' not in json_data:
                raise KeyError("no se encontro key: port")
            else:
                self.port = json_data['port']

            if 'inputDir' not in json_data:
                raise KeyError("no se encontro key: inputDir")
            else:
                self.inputDir = json_data['inputDir']

            if 'inputFileMask' not in json_data:
                raise KeyError("no se encontro key: inputFileMask")
            else:
                self.__inputFileMask = json_data['inputFileMask']

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
                self.__maxSeqNumber = 10 ** int(number_of_digits) - 1
            self.update_output_file()

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_address = (self.host, self.port)
            self.socket.connect(self.server_address)


    def write_pcap_in_file(self):

        wrpcap(self.outputFile, self.pkt)
        self.__number_of_files_w = self.__number_of_files + 1
        self.pkt = []

    def send_reg(self):

        files = (glob.glob(self.inputDir + self.__inputFileMask + "*." + self.__outputExt)).pop()
        file=rdpcap(files)
        print(files)
        for msg in file:
            print("sending: " + str(len(msg)) + " bytes")
            self.socket.send(raw(msg))
            data = self.socket.recv(2048)
            print("received: ", data.decode())
