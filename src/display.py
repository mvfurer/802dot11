import json
from influxdb import InfluxDBClient
from datetime import datetime as dt
from datetime import timedelta
import pdb
"""
Esta es una tool solo para observar lo que se escribe en la D
"""

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
# print(json.dumps(nets,  sort_keys=True, indent=4))

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'nets')
max_time = dt.now()
min_time = dt.now() - timedelta(minutes=5)
filter_ssid = 'lobo399'
query = 'select rssi, channel from signal_level where ssid = \'' + filter_ssid + '\'' +\
    ' and time > \'' + min_time.strftime("%Y-%m-%dT%H:%M:%SZ") + '\' and ' + \
        'time <  \'' + max_time.strftime("%Y-%m-%dT%H:%M:%SZ") + '\' ' + \
        'group by ssid ORDER BY time asc'
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
for r in result.get_points():
    print(r['time'])

for idx, rec in enumerate(result):
    # second element of tuple: ('signal_level', {'ssid': 'myname'})
    key_time = '{:40s}'.format(rec[idx]['time'])
    info_net = '{:20s}'.format(str(rec[idx]['rssi']))
    info_net += '{:14s}'.format(str(rec[idx]['channel']))
    nets[key_time] = info_net
print(nets)
