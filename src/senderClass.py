#!/usr/bin/env python

"""
clase sender que envia los paquetes guardados en pcap file
basado en el programa

"""
from scapy.all import *
import socket
import sys
import argparse
import json
import glob
import datetime
import pickle
from dataUtilsClass import dataUtils
from influxdb import InfluxDBClient


class Sender(dataUtils):

    def __init__(self, conf_file):
        self.conf = {
            'cfgFromFile': {
                'host': '',
                'port': 5000,
                'inputDir': '',
                'inputFileMask': '',
                'outputDir': '',
                'outputFileMask': '',
                'outputExt': '',
                'size': 0,
                "seqDig": 0
            },
            'cfgFromProc': {
                'configFile': conf_file,
                'outputFile': '',
                'readPackets': 0,
                'writePackets': 0,
                'seqNumber': 0,
                'maxSeqNumber': 0,
                'number_of_files_w': 0,
                'number_of_files_r': 0,
                'backlog': 1,
                'data_payload': 0,
                'send_file_name': ''
            }
        }
        self.class_name = "receiverClass"
        self.BUFFER_SIZE = 8 * 1024
        self.pkt = []

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
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_address = (self.conf['cfgFromFile']['host'], self.conf['cfgFromFile']['port'])
            self.socket.connect(self.server_address)

    def send_tcp(self):
        print("send_tcp buscando archivos")

        file_list = glob.glob(self.conf['cfgFromFile']['inputDir'] +
                                              self.conf['cfgFromFile']['inputFileMask'] +
                                              "*." + self.conf['cfgFromFile']['outputExt'])
        for file in file_list:
            i = 0
            # Muestro archivo de entrada completo
            self.conf['cfgFromProc']['send_file_name'] = file
            print(file)
            # extraigo el directorio y me quedo solo con el nombre de archivo
            file_name = os.path.basename(file)
            # creo el container
            container={'type': 0, 'name': file, 'payload': b'0'}
            # open file and send it
            data = ''
            with open(file, 'rb') as f:
                data_send = f.read(self.BUFFER_SIZE)
                while data_send:
                    container['payload'] = data_send

                    self.socket.sendall(pickle.dumps(container))
                    data = self.socket.recv(self.BUFFER_SIZE)
                    i = i + 1
                    data_send = f.read(self.BUFFER_SIZE)
            # it was last register. send 1 to notify
            print("sent all registers: " + str(i))
            container['type'] = 1
            container['payload'] = b'0'
            self.socket.sendall(pickle.dumps(container))
            data = self.socket.recv(self.BUFFER_SIZE)
            #self.socket.close()
        print("no more files to send")
        print("send 2 to server")
        container['type'] = 2
        container['payload'] = b'0'
        container['name'] = ''
        self.socket.sendall(pickle.dumps(container))
        data = self.socket.recv(self.BUFFER_SIZE)
        # print("Closing connection to the server ...")


    def send_db(self):
        client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example2')
        client.create_database('example2')

        f = dataUtils.open_pcap_file("/home/newheres/datacom/out/file802dot11_20190111_221608_00000.pcap")
        for reg in f:
            data = dataUtils.get_json_from_radioTap(reg)
            if len(data) > 2:
                print("[Sender] ", data)
                json_body = [data]
                print(type(json_body))
                client.write_points(json_body)
        self.set_sequence_number(self.get_next_sequence_number())

