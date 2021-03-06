#!/usr/bin/env python

"""
clase sender que envia los paquetes guardados en pcap file
basado en el programa

"""
from scapy.all import *
import socket
import sys
import json
import glob
import datetime
import signal
import pickle
from shutil import copyfile
from dataUtilsClass import dataUtils
from influxdb import InfluxDBClient
import logging
# import pdb


class Sender(dataUtils):

    def __init__(self, conf_file):
        self.conf = {
            'cfgFromFile': {
                'type': '',
                'host': '',
                'port': 5000,
                'dbName': '',
                'logFile': '',
                'inputDir': '',
                'inputFileMask': '',
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
                'backlog': 1,
                'data_payload': 0,
                'send_file_name': ''
            }
        }
        self.class_name = "receiverClass"
        self.BUFFER_SIZE = 1 * 1024
        self.pkt = []
        self.shutdown_flag = False

    def initialize(self):
        TIMEOUT = 3
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
            logging.basicConfig(filename=self.conf['cfgFromFile']['logFile'],
                                filemode='a',
                                format='%(asctime)s - %(process)d - %(levelname)s - %(message)s',
                                level=logging.DEBUG)
            if self.conf['cfgFromFile']['type'] == 'tcp':
                logging.info('connecting to: ' + self.conf['cfgFromFile']['host'] +
                             ':' + str(self.conf['cfgFromFile']['port']) +
                             ' timeout: ' + str(TIMEOUT))
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_address = (self.conf['cfgFromFile']['host'], self.conf['cfgFromFile']['port'])
                try:
                    self.socket.settimeout(TIMEOUT)
                    self.socket.connect(self.server_address)
                    logging.debug('connection success')
                except socket.gaierror as e:
                    logging.error('error connecting to: ' +
                                  self.conf['cfgFromFile']['host'] +
                                  ':' + str(self.conf['cfgFromFile']['port']) +
                                  ' timeout: ' + str(TIMEOUT) + ' - exception: ' + str(e))
                    raise e
                except socket.error as ex:
                    logging.error('socket error, connecting to: ' +
                                  self.conf['cfgFromFile']['host'] +
                                  ':' + str(self.conf['cfgFromFile']['port']) +
                                  ' timeout: ' + str(TIMEOUT) + ' - exception: ' + str(ex))
                    raise ex
            if self.conf['cfgFromFile']['type'] == 'db':
                logging.info('connecting to influxdb')
                # init client
                # self.client = InfluxDBClient(self.conf['cfgFromFile']['host'], 8086, 'root', 'root', self.conf['cfgFromFile']['dbName'])
                self.client = InfluxDBClient(self.conf['cfgFromFile']['host'], 8086, 'root', 'root')
                if {'name': self.conf['cfgFromFile']['dbName']} not in self.client.get_list_database():
                    logging.info('db does not exist, creating ...')
                    self.client.create_database(self.conf['cfgFromFile']['dbName'])
                self.client.switch_database(self.conf['cfgFromFile']['dbName'])
            return 1

    def terminate_process(self, signum, frame):
        self.shutdown_flag = True
        logging.info('(SIGTERM) terminating the process')

    def received_term_sig(self):
        return self.shutdown_flag

    def send_tcp(self):
        logging.debug('sending records to remote host ...')

        file_list = glob.glob(self.conf['cfgFromFile']['inputDir'] +
                              self.conf['cfgFromFile']['inputFileMask'] +
                              "*." + self.conf['cfgFromFile']['outputExt'])
        container = {}
        for file in file_list:
            logging.debug('opening file: ' + file)
            i = 0
            # Muestro archivo de entrada completo
            self.conf['cfgFromProc']['send_file_name'] = file
            # extraigo el directorio y me quedo solo con el nombre de archivo
            file_name = os.path.basename(file)
            # creo el container
            container = {'type': 0, 'name': file, 'payload': b'0'}
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
            logging.debug('total number of records sent: ' + str(i))
            container['type'] = 1
            container['payload'] = b'0'
            self.socket.sendall(pickle.dumps(container))
            data = self.socket.recv(self.BUFFER_SIZE)
            copyfile(file, self.conf['cfgFromFile']['outputDir'] + self.rename_dst_file(file_name))
            # cambio nombre de archivo para que no lo tome en la proxima pasada
            logging.debug('rename file from: ' + file + ' to: ' + file + '.ok')
            os.rename(file, file + '.ok')
            if self.shutdown_flag:
                logging.debug('shutting down ...')
                logging.debug('no more files to send')
                logging.debug('send message NO_MORE_FILE to server')
                container['type'] = 2
                container['payload'] = b'0'
                container['name'] = ''
                try:
                    self.socket.sendall(pickle.dumps(container))
                    data = self.socket.recv(self.BUFFER_SIZE)
                    # raise Exception('shutdown')
                except Exception as e:
                    logging.debug('send_tcp - Exception: ' + str(e))
        logging.debug('no more files to send')
        logging.debug('send message NO_MORE_FILE to server')
        container['type'] = 2
        container['payload'] = b'0'
        container['name'] = ''
        try:
            self.socket.sendall(pickle.dumps(container))
            data = self.socket.recv(self.BUFFER_SIZE)
        except Exception as e:
            logging.debug('send_tcp - Exception: ' + str(e))

    def send_db(self):
        logging.debug("[send_db] searching files in: " + self.conf['cfgFromFile']['inputDir'])
        file_list = glob.glob(self.conf['cfgFromFile']['inputDir'] +
                              self.conf['cfgFromFile']['inputFileMask'] +
                              "*." + self.conf['cfgFromFile']['outputExt'])

        for file in file_list:
            i = 0
            # Muestro archivo de entrada completo
            self.conf['cfgFromProc']['send_file_name'] = file
            logging.debug("openning: " + file)
            f = self.open_pcap_file(file)
            print("opened success: " + file)
            for reg in f:
                logging.debug("record: " + str(i) + " file: " + file)
                data = self.get_json_from_radioTap(reg)
                if len(data) > 2:
                    logging.debug('writting recod in db:  ' + str(data))
                    json_body = [data]
                    # print(type(json_body))
                    self.client.write_points(json_body)
                i = i + 1
            logging.debug('rename file from: ' + file + ' to: ' + file + '.ok')
            os.rename(file, file + '.ok')
            self.set_sequence_number(self.get_next_sequence_number())

    def send_print(self):
        print("send_print")
        i = 0
        file_list = glob.glob(self.conf['cfgFromFile']['inputDir'] +
                              self.conf['cfgFromFile']['inputFileMask'] +
                              "*." + self.conf['cfgFromFile']['outputExt'])
        print(file_list)
        for file_name in file_list:
            print("")
            print("src: " + file_name)
            f = rdpcap(file_name)
            s = f.sessions()
            for ind in s:
                for packet in s[ind]:
                    i = i + 1
                    # print("lee registro numero: " + str(i))
                    # print(packet.show())
            print("registers number: " + str(i))
            i = 0
            file = os.path.basename(file_name)
            print("dst: " + self.conf['cfgFromFile']['outputDir'] + self.rename_dst_file(file))
            copyfile(file_name, self.conf['cfgFromFile']['outputDir'] + self.rename_dst_file(file))
            copyfile(file_name, file_name + '.ok')
            if self.shutdown_flag:
                raise Exception('shutdown')

    def send(self, method):
        print("method: " + method)
        if method == 'db':
            self.send_db()
        elif method == 'tcp':
            self.send_tcp()
        elif method == 'print':
            self.send_print()
        else:
            print("unknow send option: " + method)
