import json
from influxdb import InfluxDBClient
from flask import Flask
from flask import jsonify
from flask import request
# import pdb; pdb.set_trace()
app = Flask(__name__)
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
@app.route("/networks")
def hello():
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'aps')
    query = 'select * from signal_level group by ssid ORDER BY time DESC limit 1'
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
        newkey = result.keys()[idx][SSID]['ssid']  # second element of tuple: ('signal_level', {'ssid': 'myname'})
        info_net = list()
        info_net.append(rec[0]['time'])
        info_net.append(rec[0]['rssi'])
        info_net.append(rec[0]['mac'])
        info_net.append(rec[0]['frequency'])
        info_net.append(rec[0]['channel'])
        nets[newkey] = info_net
    return jsonify(nets)
    # return json.dumps(data)


@app.route("/networks")
def hello():
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'aps')
    query = 'select * from signal_level group by ssid ORDER BY time DESC limit 1'
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
        newkey = result.keys()[idx][SSID]['ssid']  # second element of tuple: ('signal_level', {'ssid': 'myname'})
        info_net = list()
        info_net.append(rec[0]['time'])
        info_net.append(rec[0]['rssi'])
        info_net.append(rec[0]['mac'])
        info_net.append(rec[0]['frequency'])
        info_net.append(rec[0]['channel'])
        nets[newkey] = info_net
    return jsonify(nets)
    # return json.dumps(data)
