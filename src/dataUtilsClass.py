from scapy.all import *
import json
import datetime


class dataUtils:

    def __init__(self):
        pass

    def open_pcap_file(self, file_name):
        return rdpcap(file_name)

    def get_json_from_radioTap(self, pkt):
        net_name = pkt[3].info.decode("utf-8")
        tstamp = datetime.datetime.fromtimestamp(pkt[0].time).strftime('%Y-%m-%dT%H:%M:%SZ')
        dBm = pkt[0].dBm_AntSignal
        data = {"time": tstamp, "net": net_name, "dBm": dBm}
        return json.dumps(data)
