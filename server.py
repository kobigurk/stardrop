from generate_vote_data import generate_vote_data
from re import sub
import db
from unblind import unblind
import flask
from generate_keypair import generate_keypair
from sign_token import sign_token
from blind import blind
from flask import request, jsonify
import subprocess
from flask_cors import CORS
from end_commitment_phase import end_commitment_phase
from end_vote_phase import end_vote_phase
from submit_key import submit_key
import sys


# Address of the smart-contract. Empty in the beginning, set by `deploy_contract()`
contract_addr = ""

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# print("Generating human list...")
# humanlistProcess = subprocess.run(['node', 'getHumanList.js'])
# if humanlistProcess.returncode != 0:
# print("Failed to generate human list. Exiting")
# sys.exit(1)
# print("Generated human list!")

# print("Creating database")
# db.makeDB()
# print("Database successfully created")
(serv_priv_key, serv_pub_key) = generate_keypair()
print("Server keypair succesfully created: private: {}, public: {}".format(
      serv_priv_key, serv_pub_key))


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def deploy_contract():
    print("Compiling...")
    compilation = subprocess.run(['starknet-compile', 'contract.cairo',
                                  '--output=contract_compiled.json', '--abi=contract_abi.json'], stdout=subprocess.PIPE)
    if compilation.returncode != 0:
        return compilation.returncode, 201
    print("Compilation done.")

    print("Deploying...")
    deployment = subprocess.run(
        ['starknet', 'deploy', '--contract', 'contract_compiled.json', '--network', 'alpha'], stdout=subprocess.PIPE)
    if deployment.returncode != 0:
        print("Error while deploying: ", deployment.returncode)
        print(deployment.stderr.decode('utf-8'))
        sys.exit(1)
    print("Deployment done.")
    out = deployment.stdout.decode('utf-8')

    # Dirty hack to extract contract address from process output.
    print(out.split('\n'))
    print(out.split('\n')[1])
    contract_addr = out.split('\n')[1][18:18+64]
    print(contract_addr)


def initialize():
    print("Init...")
    init = subprocess.run(['starknet',  'invoke', '--address', contract_addr,
                          '--abi', 'contract_abi.json', '--function', 'initialize', '--inputs', serv_pub_key])
    if init.returncode != 0:
        return init.returncode, 201
    print("Init done")


# Easter egg
@ app.route('/', methods=['GET'])
def home():
    return "<h1>Wassu wassu wassu wassu wassu wassu wassuuuuuuuuupppppp!!!</h1>"


@ app.route('/api/sign_blinded_request', methods=['POST'])
def sign_blinded_request():
    # Dunno why get_json() doesn't work when called from `local.py`
    data = request.form
    if 'blinded_request' not in data:
        return 'Error: no blinded request provided', 201
    blinded_request = int(data['blinded_request'])
    (blinded_token, c, r) = sign_token(serv_priv_key, blinded_request)
    return ({'blinded_token': blinded_token, 'c': c, 'r': r})


@ app.route('/api/get_serv_public_key', methods=['GET'])
def get_serv_public_key():
    return ({'public_key': serv_pub_key})


# Submits the server key to the smart contract.
def key_submission():
    (r, s) = submit_key(serv_priv_key)
    # ret = subprocess.run(['starknet', 'invoke', '--address', contract_addr, '--abi',
    #                      'contract_abi.json', '--function', 'submit_key', '--inputs', serv_priv_key, r, s])
    # if (ret.returncode != 0):
    #     return 'Error: submit key unsuccessful', 204
    return "Key submission OK"


@ app.route('/api/end_commit_phase', methods=['POST'])
def end_commit_phase():
    data = request.get_json()
    if 'message' not in data:
        return "Error: missing message!", 201
    message = data['message']

    # Dumb check to reduce the chance of a random guy ending the commit phase. Not secure, only used for POC presentation.
    if message != 'vitalik<3':
        return "Nice try feds!", 202

    (r, s) = end_commitment_phase(serv_priv_key)
    # ret = subprocess.run(['starknet', 'invoke', '--address', contract_addr, '--abi',
    #                       'contract_abi.json', '--function', 'end_commitment_phase', '--inputs', r, s])
    # if (ret.returncode != 0):
    #     return 'Error: end_commit_phase unsuccessful', 203

    key_submission_result = key_submission()

    return key_submission_result


@ app.route('/api/end_voting_phase', methods=['POST'])
def end_voting_phase():
    data = request.get_json()
    if 'message' not in data:
        return "Error: missing message!", 201

    message = data['message']

    # Dumb check to reduce the chance of a random guy ending the commit phase. Not secure, only used for POC presentation.
    if message != 'vitalik<3':
        return "Nice try feds!", 202

    (r, s) = end_vote_phase(serv_priv_key)
    # ret = subprocess.run(['starknet', 'invoke', '--address', contract_addr, '--abi',
    #                      'contract_abi.json', '--function', 'end_voting_phase', '--inputs', r, s])

    # if (ret.returncode != 0):
    #     return 'Error: end voting phase unsuccessful', 203
    return "End voting phase OK"


@ app.route('/api/vote', methods=['POST'])
def vote():
    data = request.format
    if 'public_key' not in data:
        return "Error: no public key provided", 201
    if 'commit_token' not in data:
        return "Error: no commit token provided", 202
    if 'vote' not in data:
        return "Error: no vote provided", 203

    public_key = data['public_key']
    commit_token = data['commit_token']
    vote = data['vote']

    if vote == 'Yes':
        vote = 1
    elif vote == "No":
        vote = 0
    else:
        return "Error: invalid vote {}".format(vote), 204

    (hint_token_y, serv_priv_key_decomposition) = generate_vote_data(
        public_key, commit_token)
    arguments = ['starknet', 'invoke', '--address', contract_addr, '--abi', 'contract_abi.json',
                 '--function', 'cast_vote', '--inputs', serv_pub_key, hint_token_y] + serv_priv_key_decomposition
    # ret = subprocess.run(arguments)
    # if (ret.returncode != 0):
    # return 'Vote unsuccessful', 205
    return "Vote OK"

# deploy_contract()

# initialize()


app.run(host="0.0.0.0", port=int(5000))
