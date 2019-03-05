import json
from influxdb import InfluxDBClient
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'eventsdb')
    query='select * from signal_level group by network ORDER BY time DESC limit 1'
    result = client.query(query)
    data = {}
    k = 0
    for i in result:
        newkey = result.keys()[k][1]['network']
        data[newkey] = i[0]['dBm']
        k = k + 1

    return json.dumps(data)
