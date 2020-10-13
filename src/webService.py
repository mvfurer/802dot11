import json
from influxdb import InfluxDBClient
from flask import Flask
from flask import jsonify
from flask import request
from datetime import datetime as dt
from datetime import timedelta

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

'''
query: select * from signal_level group by ssid ORDER BY time DESC limit 1
ResultSet({'('signal_level', {'ssid': 'myname'})': [{'time': '2020-08-23T19:16:57Z', 'channel': '6', 'devId': 0,
 'frequency': '2437', 'mac': '88:02:dd:66:ca:00', 'rssi': '-55'}],
  '('signal_level', {'ssid': 'yourName 2.4GHz'})': [{'time': '2020-08-23T19:12:56Z', 'channel': '11', 'devId': 0,
   'frequency': '2462', 'mac': 'ff:00:99:4b:c3:77', 'rssi': '-83'}], ..... }]})
'''


@app.route("/networks", methods=['GET'])
def networks():
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'nets')
    query = 'select * from signal_level group by ssid ORDER BY time desc limit 1'
    result = client.query(query)
    nets = {}
    SSID = 1
    for idx, rec in enumerate(result):
        # second element of tuple: ('signal_level', {'ssid': 'myname'})
        newkey = '{:40s}'.format(result.keys()[idx][SSID]['ssid'])
        info_net = '{:22s}'.format(rec[0]['time'])
        info_net += '{:5s}'.format(str(rec[0]['rssi']))
        info_net += '{:19s}'.format(rec[0]['mac'])
        info_net += '{:4s}'.format(rec[0]['channel'])
        info_net += '{:6s}'.format(rec[0]['frequency'])
        nets[newkey] = info_net
    return jsonify(nets)


@app.route('/stats', methods=['POST'])
def stats():
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'nets')
    query = 'select * from signal_level group by ssid ORDER BY time desc limit 1'
    result = client.query(query)
    nets = {}
    SSID = 1
    for idx, rec in enumerate(result):
        # second element of tuple: ('signal_level', {'ssid': 'myname'})
        newkey = '{:40s}'.format(result.keys()[idx][SSID]['ssid'])
        info_net = '{:22s}'.format(rec[0]['time'])
        info_net += '{:5s}'.format(str(rec[0]['rssi']))
        info_net += '{:19s}'.format(rec[0]['mac'])
        info_net += '{:4s}'.format(rec[0]['channel'])
        info_net += '{:6s}'.format(rec[0]['frequency'])
        nets[newkey] = info_net
    return jsonify(nets)


@app.route('/last', methods=['POST'])
def last():
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    if request.method == 'POST':
        data = request.get_json()
        nets = {}
        if (data is None) or ('range' not in data.keys()):
            return jsonify(nets)
        client = InfluxDBClient('localhost', 8086, 'root', 'root', 'nets')
        last_time = dt.now() - timedelta(minutes=data['range'])
        query = 'select * from signal_level where time > \'' + \
                last_time.strftime("%Y-%m-%dT%H:%M:%SZ") + '\' group by ssid ORDER BY time desc limit 1'
        result = client.query(query)

        SSID = 1
        for idx, rec in enumerate(result):
            # second element of tuple: ('signal_level', {'ssid': 'myname'})
            newkey = '{:30s}'.format(result.keys()[idx][SSID]['ssid'])
            info_net = '{:22s}'.format(rec[0]['time'])
            info_net += '{:5s}'.format(str(rec[0]['rssi']))
            info_net += '{:19s}'.format(rec[0]['mac'])
            info_net += '{:4s}'.format(rec[0]['channel'])
            info_net += '{:6s}'.format(rec[0]['frequency'])
            nets[newkey] = info_net
        return jsonify(nets)


@app.route('/mean', methods=['POST'])
def mean():
    if request.method == 'POST':
        data = request.get_json()
        nets = {}
        client = InfluxDBClient('localhost', 8086, 'root', 'root', 'nets')
        if (data is None) or ('range' not in data.keys()):
            return jsonify(nets)
        max_time = dt.now()
        min_time = dt.now() - timedelta(minutes=data['range'])
        query = 'select mean(rssi), count(rssi) from signal_level where ' + \
                'time > \'' + min_time.strftime("%Y-%m-%dT%H:%M:%SZ") + '\' and ' + \
                'time <  \'' + max_time.strftime("%Y-%m-%dT%H:%M:%SZ") + '\' ' + \
                'group by ssid ORDER BY time desc limit 1'
        print(query)
        result = client.query(query)
        SSID = 1
        for idx, rec in enumerate(result):
            # second element of tuple: ('signal_level', {'ssid': 'myname'})
            newkey = '{:30s}'.format(result.keys()[idx][SSID]['ssid'])
            info_net = '{:25s}'.format(rec[0]['time'].split('.')[0] + 'Z')
            info_net += '{:10s}'.format(str(round(rec[0]['mean'], 2)))
            info_net += '{:14s}'.format(str(rec[0]['count']))
            nets[newkey] = info_net
        return jsonify(nets)


@app.route('/history', methods=['POST'])
def history():
    if request.method == 'POST':
        data = request.get_json()
        nets = {}
        client = InfluxDBClient('localhost', 8086, 'root', 'root', 'nets')
        if (data is None) or ('range' not in data.keys()) or ('ssid' not in data.keys()):
            return jsonify(nets)
        max_time = dt.now()
        min_time = dt.now() - timedelta(minutes=data['range'])
        filter_ssid = data['ssid']
        query = 'select rssi, channel from signal_level where ssid = \'' + filter_ssid + '\'' +\
                ' and time > \'' + min_time.strftime("%Y-%m-%dT%H:%M:%SZ") + '\' and ' + \
                'time <  \'' + max_time.strftime("%Y-%m-%dT%H:%M:%SZ") + '\' ' + \
                'group by ssid ORDER BY time desc'
        print(query)
        result = client.query(query)
        for rec in result.get_points():
            # second element of tuple: ('signal_level', {'ssid': 'myname'})
            newkey = '{:25s}'.format(rec['time'])
            info_net = '{:10s}'.format(str(rec['rssi']))
            info_net += '{:4s}'.format(rec['channel'])
            nets[newkey] = info_net
        return jsonify(nets)


if __name__ == '__main__':
    app.run(debug=True)
