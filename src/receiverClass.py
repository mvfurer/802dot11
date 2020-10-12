#!/usr/bin/env python

"""
clase sender que envia los paquetes guardados en pcap file
basado en el programa echo server del libro
Python Network Programming Cookbook -- Chapter – 1

"""
from scapy.all import *
import socket
import sys
import argparse
import json
import glob
import signal
import datetime
import pickle
import os
from dataUtilsClass import dataUtils
import logging


class Receiver(dataUtils):

    def __init__(self, conf_file):
        self.conf = {
            'cfgFromFile': {
                'host': '',
                'src_port': 5000,
                'logFile': '',
                'outputDir': '',
                'outputFileMask': '',
                'outputExt': '',
                'tmpOutputExt': '',
                'size': 0,
                "seqDig": 0
            },
            'cfgFromProc': {
                'configFile': conf_file,
                'outputFile': '',
                'tmpOutputFile': '',
                'readPackets': 0,
                'writePackets': 0,
                'seqNumber': 0,
                'maxSeqNumber': 0,
                'number_of_files_w': 0,
                'number_of_files_r': 0,
                'backlog': 1
            }
        }
        self.data_payload = 2 * 1024
        self.class_name = "receiverClass"
        self.pkt = []
        self.shutdown_flag = False

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

            logging.basicConfig(filename=self.conf['cfgFromFile']['logFile'],
                                filemode='a',
                                format='%(asctime)s - %(process)d - %(levelname)s - %(message)s',
                                level=logging.DEBUG)
            number_of_digits = self.conf['cfgFromFile']['seqDig']
            self.conf['cfgFromProc']['maxSeqNumber'] = 10 ** int(number_of_digits) - 1
            self.conf['cfgFromProc']['seqNumber'] = 0
            self.update_output_file()
            """ A simple echo server """
            logging.info('watting income connections ...')
            logging.info('creatting socket server ...')
            # Create a TCP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Enable reuse address/port
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind the socket to the port
            self.server_address = (self.conf['cfgFromFile']['host'], self.conf['cfgFromFile']['src_port'])
            # print
            # "Starting up echo server on %s port %s" % server_address
            logging.info('bind socket server ...')
            self.sock.bind(self.server_address)
            # Listen to clients, backlog argument specifies the max no. of queued connections
            logging.info('listen socket server ...')
            self.sock.listen(self.conf['cfgFromProc']['backlog'])
            print("Waiting to receive message from client")
            logging.info('accept socket server ...')
            self.client, self.address = self.sock.accept()

    def terminate_process(self, signum, frame):
        self.shutdown_flag = True
        logging.info('(SIGTERM) terminating the process')

    def received_term_sig(self):
        return self.shutdown_flag

    def start(self):

        i = 0
        self.data = []
        while not self.received_term_sig():
            try:
                container = self.client.recv(self.data_payload)
                logging.debug('received message')
                datarcv = pickle.loads(container)
                if datarcv['type'] == 0:
                    logging.debug('received OK')
                    self.data = datarcv['payload']
                    self.pkt.append(self.data)
                    i = i + 1
                    self.client.send('OK'.encode())
                    logging.debug('sent  OK')
                elif datarcv['type'] == 1:
                    logging.debug('received all registries: ' + str(i))
                    file_name = os.path.basename(datarcv['name'])
                    self.conf['cfgFromProc']['outputFile'] = self.conf['cfgFromFile']['outputDir'] + \
                                                             self.conf['cfgFromFile']['outputFileMask'] + \
                                                             file_name.split('_', 1)[1]
                    logging.debug("write outputfile: " + self.conf['cfgFromProc']['outputFile'])
                    self.client.send('OK_CLOSE'.encode())
                    logging.debug('sent OK_CLOSE')
                    self.write_pcap_in_file()
                    self.pkt = []
                    i = 0
                else:
                    self.pkt = []
                    self.client.send('OK_CLOSE'.encode())
                    logging.debug("received all registries")
                    # cierra la conexion, reicibio el fin de envio
                    # print("Cerrando conexion  ... ")
                    # self.client.close()
                    break
                    # self.client, self.address = self.sock.accept()
            except Exception as e:
                logging.debug('Exception: process ' + str(e))
                time.sleep(5)

    def send_reg(self):

        files = (glob.glob(self.inputDir + self.__inputFileMask + "*." + self.__outputExt)).pop()
        file = rdpcap(files)
        logging.debug(files)
        for msg in file:
            logging.debug("sending: " + str(len(msg)) + " bytes")
            self.socket.send(raw(msg))
            data = self.socket.recv(2048)
            print("received: ", data.decode())
