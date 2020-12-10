"""
Este script es una tool para trabajar con influxdb
"""
import json
from influxdb import InfluxDBClient
from datetime import datetime as dt
from datetime import timedelta
import pdb

'''
data points:
data = {
        "measurement": "signal_level",
        "time": tstamp,
        "tags": {
            "ssid": net_name,
            "mac": mac,
            "rssi": dBm,
            "channel": channel,
            "frequency": freq
        },
        "fields": {
            "devId": 0
        }
    }
'''

# client = InfluxDBClient('localhost', 8086, 'root', 'root', 'nets')
# query='select * from signal_level group by ssid ORDER BY time DESC limit 1'
# result = client.query(query)
# nets = {}
'''
query: select * from signal_level group by ssid ORDER BY time DESC limit 1
ResultSet({'('signal_level', {'ssid': 'myname'})': [{'time': '2020-08-23T19:16:57Z', 'channel': '6', 'devId': 0,
 'frequency': '2437', 'mac': '88:02:dd:66:ca:00', 'rssi': '-55'}],
  '('signal_level', {'ssid': 'yourName 2.4GHz'})': [{'time': '2020-08-23T19:12:56Z', 'channel': '11', 'devId': 0,
   'frequency': '2462', 'mac': 'ff:00:99:4b:c3:77', 'rssi': '-83'}], ..... }]})
'''
# SSID = 1
#
# for idx, rec in enumerate(result):
#     newkey = result.keys()[idx][SSID]['ssid']  # second element of tuple: ('signal_level', {'ssid': 'myname'})
#     info_net = list()
#     info_net.append(rec[0]['time'])
#     info_net.append(rec[0]['rssi'])
#     info_net.append(rec[0]['mac'])
#     info_net.append(rec[0]['frequency'])
#     info_net.append(rec[0]['channel'])
#     nets[newkey] = info_net
#print(json.dumps(nets,  sort_keys=True, indent=4))
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'nets')
max_time = dt.now()
min_time = dt.now() - timedelta(minutes=5)
query = 'select mean(rssi), count(rssi) from signal_level where ' + \
        'time > \'' + min_time.strftime("%Y-%m-%dT%H:%M:%SZ") + '\' and ' + \
        'time <  \'' + max_time.strftime("%Y-%m-%dT%H:%M:%SZ") + '\' ' + \
        'group by ssid ORDER BY time desc limit 1'
# query='select * from signal_level group by ssid ORDER BY time DESC limit 1'
result = client.query(query)
nets = {}
'''
query: select * from signal_level group by ssid ORDER BY time DESC limit 1
ResultSet({'('signal_level', {'ssid': 'myname'})': [{'time': '2020-08-23T19:16:57Z', 'channel': '6', 'devId': 0,
 'frequency': '2437', 'mac': '88:02:dd:66:ca:00', 'rssi': '-55'}],
  '('signal_level', {'ssid': 'yourName 2.4GHz'})': [{'time': '2020-08-23T19:12:56Z', 'channel': '11', 'devId': 0,
   'frequency': '2462', 'mac': 'ff:00:99:4b:c3:77', 'rssi': '-83'}], ..... }]})
'''
SSID = 1
for idx, rec in enumerate(result):
    # second element of tuple: ('signal_level', {'ssid': 'myname'})
    newkey = '{:30s}'.format(result.keys()[idx][SSID]['ssid'])
    info_net = '{:22s}'.format(rec[0]['time'])
    info_net += '{:20s}'.format(str(rec[0]['mean']))
    info_net += '{:14s}'.format(str(rec[0]['count']))
    nets[newkey] = info_net
print(nets)