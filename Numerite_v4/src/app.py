from flask import Flask, request, jsonify, request
from json import dumps
from flask_cors import CORS
from AMWPS_pres import AMWPS

app = Flask(__name__)
CORS(app)

@app.route('/api/mwp', methods=['POST'])
def mwp():
    mwp = request.json['mwp']
    solver = AMWPS(mwp)
    solver.solve()

    solution = solver.explanation
    res = {'solution': solution}
    return dumps(res)
    
if __name__ == '__main__':
    app.run()