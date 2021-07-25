from flask import request, jsonify
from generate_keypair import generate_keypair
from blind import blind
from sign_token import sign_token
from unblind import unblind
import db
import requests
import flask
from flask_cors import CORS
from shared import LIVE_DEMO
import subprocess

SERV_URL = "http://192.168.106.112:5000"


app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@ app.route('/api/generate_keys', methods=['GET'])
def generate_keys():
    (priv, pub) = generate_keypair()
    print("Generated pub: {}\nGenerated priv: {}".format(pub, priv))
    print("str: ", str(pub), str(priv))
    return jsonify([{'private_key': str(priv), 'public_key': str(pub)}])


# Utility function that calls a node script to verify if the `signature` is indeed `message` signed by `poh_address`.
# Used to basically verify that the user is indeed the owner of poh_address.
def verify_sig(signature, message, poh_address):
    verif_process = subprocess.run(
        ['node', 'signGestion/get_signer_address.js', str(signature), str(message), str(poh_address)])
    return verif_process.returncode == 0


def get_serv_pub_key():
    pub_key_req = requests.get(SERV_URL + '/api/get_serv_public_key')
    serv_pub_key = int(pub_key_req.json()['public_key'])
    return serv_pub_key


def get_contract_address():
    contract_address_req = requests.get(SERV_URL + '/api/get_contract_address')
    contract_address = int(contract_address_req.json()['contract_address'])
    return contract_address


@ app.route('/api/generate_commit_token', methods=['POST'])
def generate_commit_token():
    data = request.get_json()
    print(data)
    if 'poh_address' not in data:
        return "Error: no address provided", 201
    if 'signature' not in data:
        return "Error: no signature provided", 202
    if 'public_key' not in data:
        return "Error: no public key provided", 203

    poh_address = data['poh_address']
    signature = data['signature']
    public_key = data['public_key']

    # Check that this the user is actually the owner of the POH address by verifying the signed message 'eip42'
    sig_is_valid = verify_sig(signature, 'eip42', poh_address)
    if not sig_is_valid:
        return "Error: invalid signature", 204

    # check that user is actually in the POH and has not already generated a commit token
    # if db.try_vote(poh_address) == False:
    #     return "Error: already voted or not in POH", 205

    (blinded_request, blinded_factor) = blind(int(public_key))

    req = {'blinded_request': blinded_request}
    res = requests.post(
        SERV_URL + '/api/sign_blinded_request', req)
    res_json = res.json()
    blinded_token = int(res_json['blinded_token'])
    c = int(res_json['c'])
    r = int(res_json['r'])

    serv_pub_key = get_serv_pub_key()

    commit_token = unblind(blinded_token, blinded_factor,
                           serv_pub_key, blinded_request, c, r)
    print("commit token: ", commit_token)

    return jsonify([{'commit_token': str(commit_token)}])


@ app.route('/api/get_result', methods=['GET'])
def get_result():
    contract_addr = get_contract_address()
    if LIVE_DEMO:
        res = subprocess.run(['starknet',  'call', '--address', contract_addr,
                              '--abi', 'contract_abi.json', '--function', 'get_result'])
        if res.returncode != 0:
            return "Error executing starknet call: exited with {}".format(res.returncode), 201
    return True


@ app.route('/', methods=['GET'])
# Easter egg
def home():
    return "<h1>My local server</h1>"


print("Starting local")
app.run(host="0.0.0.0", port=int(4242), use_reloader=False)
