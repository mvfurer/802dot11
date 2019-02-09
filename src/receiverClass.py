#!/usr/bin/env python

"""
clase sender que envia los paquetes guardados en pcap file
basado en el programa

"""
from senderClass import Sender
from scapy.all import *
import socket
import sys
import argparse
import json
import glob
import datetime
import pickle


class Receiver(Sender):

    def __init__(self, conf_file):
        self.__conf = conf_file
        self.__number_of_files_w = 0
        self.__number_of_files_r = 0
        self.backlog = 1
        self.data_payload = 9 * 1024
        self.outputFile = ''
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

            if 'src_port' not in json_data:
                raise KeyError("no se encontro key: src_port")
            else:
                self.port = json_data['src_port']

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



    def run(self):
        """ A simple echo server """
        # Create a TCP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Enable reuse address/port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to the port
        self.server_address = (self.host, self.port)
        # print
        # "Starting up echo server on %s port %s" % server_address
        self.sock.bind(self.server_address)
        # Listen to clients, backlog argument specifies the max no. of queued connections
        self.sock.listen(self.backlog)
        self.client, self.address = self.sock.accept()
        print("Waiting to receive message from client")
        i = 0
        self.data = []
        while True:
            container = self.client.recv(self.data_payload)
            print(container)
            datarcv = pickle.loads(container)
            #print(datarcv)
            if datarcv['type'] == 0:
                self.data = datarcv['payload']
                print(self.data)
                print(pickle.dumps(self.data))
                self.pkt.append(self.data)
                print("appended: ")
                print(self.pkt)
                i = i + 1
                # print("Data received  ... " + str(self.data))
                self.client.send("OK".encode())
                # print("sent OK bytes back " + str(self.address))
            elif datarcv['type'] == 1:
                print("recieved all registries: " + str(i))
                self.outputFile = self.__outputDir + datarcv['name']
                print("write outputfile: " + self.outputFile)
                print("saved file")
                self.write_pcap_in_file()
                self.pkt = []
                i = 0
            else:
                self.pkt = []
                print("recieved all registries")
                # cierra la conexion, reicibio el fin de envio
                print("Cerrando conexion  ... ")
                self.client.close()
                break
                #self.client, self.address = self.sock.accept()


    def write_pcap_in_file(self):

        with open(self.outputFile, "a+b") as f:
            for element in self.pkt:
                f.write(bytes(element))
        self.__number_of_files_w = self.__number_of_files_w + 1

    def send_reg(self):

        files = (glob.glob(self.inputDir + self.__inputFileMask + "*." + self.__outputExt)).pop()
        file=rdpcap(files)
        print(files)
        for msg in file:
            print("sending: " + str(len(msg)) + " bytes")
            self.socket.send(raw(msg))
            data = self.socket.recv(2048)
            print("received: ", data.decode())
