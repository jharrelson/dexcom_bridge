from nightscout import Api
from arrow import Arrow
from urllib import request
from flask import Flask, jsonify, request as req

application_id = 'd89443d2-327c-4a6f-89e5-496bbb0317db'
nightscout_url = ''
server_host = '0.0.0.0'
server_port = 5000

app = Flask('DexcomBridge')
nightscout_api = Api(nightscout_url)

class DexcomBridge:
    @classmethod
    def get_nightscout_data(self, count):
        return nightscout_api.get_sgvs({ 'count': count })

    @classmethod
    def nightscout_to_dexcom(self, sgvs):
        return [ {
            'DT': '/Date(' + Arrow.fromdatetime(sgv.date).format('XSSSZ') + ')/',
            'ST': '/Date(' + Arrow.fromdatetime(sgv.date).format('XSSSZ') + ')/',
            'WT': '/Date(' + Arrow.fromdatetime(sgv.date).format('XSSS') + ')/',
            'Value': int(sgv.sgv),
            'Trend': DexcomBridge.convert_slope(sgv.direction)
        } for sgv in sgvs ]

    @classmethod
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
    res = DexcomBridge.get_nightscout_data(count)
    res = DexcomBridge.nightscout_to_dexcom(res)
    return jsonify(res), 200

@app.route('/ShareWebServices/Services/General/LoginPublisherAccountByName', methods=['GET', 'POST'])
def authCheck():
    return jsonify(application_id), 200
    
if __name__ == "__main__":
    app.run(host=server_host, port=server_port)