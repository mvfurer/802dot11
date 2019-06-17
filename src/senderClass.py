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
                'type': '',
                'host': '',
                'port': 5000,
                'dbName': '',
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
        self.BUFFER_SIZE = 1 * 1024
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
            if self.conf['cfgFromFile']['type'] == 'tcp':
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_address = (self.conf['cfgFromFile']['host'], self.conf['cfgFromFile']['port'])
                self.socket.connect(self.server_address)
            if self.conf['cfgFromFile']['type'] == 'db':
                self.client = InfluxDBClient(self.conf['cfgFromFile']['host'], 8086, 'root', 'root', self.conf['cfgFromFile']['dbName'])

    def send_tcp(self):
        print("send_tcp buscando archivos")

        file_list = glob.glob(self.conf['cfgFromFile']['inputDir'] +
                                              self.conf['cfgFromFile']['inputFileMask'] +
                                              "*." + self.conf['cfgFromFile']['outputExt'])
        container = {}
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
            # cambio nombre de archivo para que no lo tome en la proxima pasada
            os.rename(file, file + '.ok')
        print("no more files to send")
        print("send 2 to server")
        container['type'] = 2
        container['payload'] = b'0'
        container['name'] = ''
        self.socket.sendall(pickle.dumps(container))
        data = self.socket.recv(self.BUFFER_SIZE)

    def send_db(self):
        f = self.open_pcap_file("/home/newheres/datacom/out/file802dot11_20190111_221608_00000.pcap")
        for reg in f:
            data = self.get_json_from_radioTap(reg)
            if len(data) > 2:
                print("[Sender] ", data)
                json_body = [data]
                print(type(json_body))
                self.client.write_points(json_body)
        self.set_sequence_number(self.get_next_sequence_number())

    def send_print(self):
        print("send_print")
        i = 0
        file_list = glob.glob(self.conf['cfgFromFile']['inputDir'] +
                              self.conf['cfgFromFile']['inputFileMask'] +
                              "*." + self.conf['cfgFromFile']['outputExt'])
        for file_name in file_list:
            print(file_name)
            f = rdpcap(file_name)
            s = f.sessions()
            for ind in s:
                for packet in s[ind]:
                    i = i + 1
                    print("lee registro numero: " + str(i))
                    print(packet.show())
        exit()

    def send(self, method):
        if method == 'db':
            self.send_db()

        if method == 'tcp':
            self.send_tcp()

        if method == 'print':
            self.send_print()
        else:
            print("unknow send option: ", method)
