from scapy.all import *
import json
import datetime
import sys


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
                    "tags": {
                        "network": net_name,
                        "dBm": dBm
                    },
                    "time": tstamp,
                    "fields": {
                        "rb_id": 0
                    }
                }

        except (IndexError, AttributeError):
            print("[dataUtils] error: ", sys.exc_info()[0] , " ocurred")
            data = {}
        return data

    def get_value_from_json(self, json_data, field):
        if field not in json_data:
            raise KeyError('no se encontro key: ', field)
        else:
            return json_data[field]

