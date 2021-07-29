from flask import request, jsonify
from generate_keypair import generate_keypair
from blind import blind
from unblind import unblind
from commit import commit
import requests
import flask
from flask_cors import CORS
from utils import INTERACT_WITH_STARKNET, print_output, launch_command, SERVER_URL, get_contract_address
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@ app.route('/api/generate_keys', methods=['GET'])
def generate_keys():
    (priv, pub) = generate_keypair()
    print("Generated pub: {}\nGenerated priv: {}".format(pub, priv))
    return jsonify([{'private_key': str(priv), 'public_key': str(pub)}])


# Utility function that calls a node script to verify if the `signature` is indeed `message` signed by `poh_address`.
# Used to basically verify that the user is indeed the owner of the `poh_address`.
def verify_sig(signature, message, poh_address):
    print("-- VERIFY SIG --\n")
    verif_process = launch_command(
        ['node', 'signGestion/get_signer_address.js', str(signature), str(message), str(poh_address)], False)
    return verif_process.returncode == 0


# Returns the server public key. This should not be exposed or used: the client should interact with the smart-contract, AFTER
# the `submit_key` phase. The server uploads his private key to the smart-contract, so there is no need for the server to expose his private key.
def get_serv_pub_key():
    pub_key_req = requests.get(SERVER_URL + '/api/get_serv_public_key')
    serv_pub_key = int(pub_key_req.json()['public_key'])
    return serv_pub_key


# Utility function that returns the contract address.
def get_contract_address():
    contract_address_req = requests.get(
        SERVER_URL + '/api/get_contract_address')
    req_json = contract_address_req.json()
    print(req_json)
    contract_address = req_json['contract_address']
    return contract_address


# Doesn't only generate the commit token but also the voting token. Would need to be renamed (`generate_tokens` maybe?)
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

    if 'force_commit' in data:
        force_commit = data['force_commit']
    else:
        force_commit = "Yes"

    poh_address = data['poh_address']
    signature = data['signature']
    public_key = data['public_key']

    # `voting token` will be the token sent when casting a vote.
    # `blinded_request` is the message we will ask the server to sign.
    # `blinded_factor` is a ratio that we will use later on to make sure that the server correctly signed the `blinded_request`.
    (voting_token, blinded_request, blinded_factor) = blind(int(public_key))

    # Ask the server to sign the blinded request.
    req = {'blinded_request': blinded_request,
           'poh_address': poh_address, 'signature': signature, 'force_commit': force_commit}
    res = requests.post(
        SERVER_URL + '/api/sign_blinded_request', req)

    if res.status_code != 200:
        return "Error: server failed to sign request", 206

    res_json = res.json()
    # Retrieve the `signed_blinded_token` from the server's response.
    signed_blinded_token = int(res_json['blinded_token'])
    c = int(res_json['c'])
    r = int(res_json['r'])

    serv_pub_key = get_serv_pub_key()

    commit_token = unblind(signed_blinded_token, blinded_factor,
                           serv_pub_key, blinded_request, c, r)
    print("commit token: ", commit_token)

    print(voting_token)
    return jsonify([{'commit_token': str(commit_token), 'voting_token': str(voting_token)}])


@ app.route('/api/commit', methods=['POST'])
def commit_to_token():
    data = request.get_json()
    print(data)
    if 'private_key' not in data:
        return "Error: missing private key", 201
    if 'commit_token' not in data:
        return "Error: missing commit token", 203

    private_key = int(data['private_key'])
    commit_token = int(data['commit_token'])

    (public_key, r, s) = commit(private_key, commit_token)
    contract_addr = get_contract_address()

    if INTERACT_WITH_STARKNET:
        print("-- COMMIT --\n")
        (_tx_id, res) = launch_command(['starknet',  'invoke', '--address', contract_addr,
                                       '--abi', 'contract/contract_abi.json', '--network', 'alpha', '--function', 'commit', '--inputs', str(public_key), str(commit_token), str(r), str(s)], True)
        print_output(res)
        if res.returncode != 0:
            print(res.stderr.decode('utf-8'))
            return "Error executing starknet call: exited with {}".format(res.returncode), 204
    else:
        time.sleep(8)
    return "OK"


@ app.route('/', methods=['GET'])
# Easter egg
def home():
    return "<h1>My local server</h1>"


print("Starting local")
app.run(host="0.0.0.0", port=int(4242), use_reloader=False)
