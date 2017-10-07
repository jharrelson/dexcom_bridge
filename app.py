import json
import uuid
from arrow import Arrow
from datetime import datetime
from urllib import request
from flask import Flask, jsonify, request as req

app = Flask('DexcomBridge')

applicationId = 'd89443d2-327c-4a6f-89e5-496bbb0317db'
base_url = ''
server_host = '0.0.0.0'
server_port = 5000

class DexcomBridge:
    def get_nightscout_data(self, count):
        url = base_url + '/pebble?count=' + count + '&units=mgdl'
        res = request.urlopen(url).read()

        return res

    def nightscout_to_dexcom(self, nightscout_data):
        nightscout_dict = json.loads(str(nightscout_data, 'utf-8'))
        arr = []
        for k in nightscout_dict['bgs']:
            d = {}
            d['DT'] = '/Date(' + Arrow.fromtimestamp(k['datetime'] / 1000).format('XSSSZ') + ')/' 
            d['ST'] = '/Date(' + Arrow.fromtimestamp(k['datetime'] / 1000).format('XSSSZ') + ')/' 
            d['WT'] = '/Date(' + Arrow.utcfromtimestamp(k['datetime'] / 1000).format('XSSS') + ')/' 
            d['Value'] = int(k['sgv'])
            d['Trend'] = self.convert_slope(k['direction'])
            arr.append(d)
        return arr

    def convert_slope(self, direction):
        return  {
                    'DoubleUp': 1,
                    'SingleUp': 2,
                    'FortyFiveUp': 3,
                    'Flat': 4,
                    'FortyFiveDown': 5,
                    'SingleDown': 6,
                    'DoubleDown': 7,
                    'NOT COMPUTABLE': 8,
                    'OUT OF RANGE': 9,
                    'None': 0
                }.get(direction, 0)

@app.route('/ShareWebServices/Services/Publisher/ReadPublisherLatestGlucoseValues', methods=['GET', 'POST'])
def index():
    count = req.args.get('maxCount', 3)
    bridge = DexcomBridge()
    res = bridge.get_nightscout_data(count)
    res = bridge.nightscout_to_dexcom(res)
    return jsonify(res), 200

@app.route('/ShareWebServices/Services/General/LoginPublisherAccountByName', methods=['GET', 'POST'])
def authCheck():
    return jsonify(applicationId), 200
    
if __name__ == "__main__":
    app.run(host=server_host, port=server_port)