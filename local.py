from flask import request, jsonify
from generate_keypair import generate_keypair
from blind import blind
from sign_token import sign_token
from unblind import unblind
import db
import requests
import flask
from flask_cors import CORS

SERV_URL = "http://192.168.0.44:5000"


app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@ app.route('/api/generate_keys', methods=['GET'])
def generate_keys():
    (priv, pub) = generate_keypair()
    return jsonify([{'private_key': priv, 'public_key': pub}])


@ app.route('/api/generate_commit_token', methods=['POST'])
def generate_commit_token():
    if 'poh_address' not in request.form:
        return "Error: no address provided", 201
    if 'signature' not in request.form:
        return "Error: no signature provided", 202

    poh_address = request.form['poh_address']
    print(type(poh_address))
    signature = request.form['signature']

    # check here with node

    if db.try_vote(poh_address) == False:
        return "Error: already voted or not in POH", 202

    (_priv, pub) = generate_keypair()

    (blinded_request, blinded_factor) = blind(pub)

    req = {'blinded_request': blinded_request}
    res = requests.post(
        SERV_URL + '/api/sign_blinded_request', data=req)
    res_json = res.json()
    blinded_token = int(res_json['blinded_token'])
    c = int(res_json['c'])
    r = int(res_json['r'])

    pub_key_req = requests.get(SERV_URL + '/api/get_serv_public_key')
    serv_pub_key = int(pub_key_req.json()['public_key'])

    commit_token = unblind(blinded_token, blinded_factor,
                           serv_pub_key, blinded_request, c, r)

    return jsonify([{'commit_token': commit_token}])
