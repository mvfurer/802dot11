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
import pickle


class Sender(Collector):

    def __init__(self, conf_file):
        self.__conf = conf_file
        self.__number_of_files_w = 0
        self.__number_of_files_r = 0
        self.send_file_name = ''
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

        for self.send_file_name in (glob.glob(self.inputDir + self.__inputFileMask + "*." + self.__outputExt)):
            i = 0
            # Muestro archivo de entrada completo
            print(self.send_file_name)
            # extraigo el directorio y me quedo solo con el nombre de archivo
            file_name = os.path.basename(self.send_file_name)
            # file=rdpcap(self.send_file_name)
            # creo el container
            container={'type': 0, 'name': file_name, 'payload': b'0'}
            with open(self.send_file_name, 'rb') as f:
                data_send = f.read(8 * 1024)
                while data_send:
                    container['payload'] = data_send
                    self.socket.sendall(pickle.dumps(container))
                    data = self.socket.recv(8 * 1024)
                    i = i + 1
                    data_send = f.read(8 * 1024)
            print("sent all registers: " + str(i))
            container['type'] = 1
            container['payload'] = b'0'
            self.socket.sendall(pickle.dumps(container))
        print("no more files to send")
        container['type'] = 2
        container['payload'] = b'0'
        container['name'] = ''
        self.socket.sendall(pickle.dumps(container))
        print("Closing connection to the server ...")
        self.socket.close()