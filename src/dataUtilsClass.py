from scapy.all import *
import json
import datetime
import sys
import pwd
import grp
import os

class dataUtils:

    def __init__(self):
        pass

    def open_pcap_file(self, file_name):
        return rdpcap(file_name)

    def get_json_from_radioTap(self, pkt):
        try:
            net_name = pkt[3].info.decode("utf-8")
            tstamp = datetime.datetime.fromtimestamp(pkt[0].time).strftime('%Y-%m-%dT%H:%M:%SZ')
            dBm = pkt[0].dBm_AntSignal
            data = {
                    "measurement": "signal_level",
                    "time": tstamp,
                    "tags": {
                        "network": net_name,
                        "dBm": dBm
                    },
                    "fields": {
                        "devId": 0
                    }
                }

        except (IndexError, AttributeError):
            print("[dataUtils] error: ", sys.exc_info()[0] , " ocurred")
            data = {}
        return data

    def get_value_from_json(self, json_data, key):
        if key not in json_data:
            raise KeyError('no se encontro key: ', key)
        else:
            return json_data[key]

    def write_pcap_in_file(self):
        if not os.path.isfile(self.conf['cfgFromProc']['outputFile']):
            with open(self.conf['cfgFromProc']['outputFile'], "a+b") as f:
                for element in self.pkt:
                    f.write(bytes(element))
            self.conf['cfgFromProc']['number_of_files_w'] = self.conf['cfgFromProc']['number_of_files_w'] + 1
        else:
            print('[' + self.class_name + '] ' + self.conf['cfgFromProc']['outputFile'] + ' already exist. skipping')
        self.set_sequence_number(self.get_next_sequence_number())

    def write_dot11_in_pcap(self):
        wrpcap(self.conf['cfgFromProc']['outputFile'], self.pkt)
        machine = os.uname()[4]
        if machine == "x86_64":
            uid = pwd.getpwnam("newheres").pw_uid
            gid = grp.getgrnam("newheres").gr_gid
        else: # just guessing is arm
            uid = pwd.getpwnam("pi").pw_uid
            gid = grp.getgrnam("pi").gr_gid
        os.chown(self.conf['cfgFromProc']['outputFile'], uid, gid)
        self.set_sequence_number(self.get_next_sequence_number())

    def update_output_file(self):
        now = datetime.datetime.now()
        self.conf['cfgFromProc']['outputFile'] = self.conf['cfgFromFile']['outputDir'] + \
                                                 self.conf['cfgFromFile']['outputFileMask'] + \
                                                 now.strftime("%Y%m%d_%H%M%S") + "_" + \
                                                 format(self.conf['cfgFromProc']['seqNumber'], "05d") + \
                                                 "." + self.conf['cfgFromFile']['outputExt']

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
