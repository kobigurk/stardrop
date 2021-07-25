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
from shared import COMPILE_CONTRACT, DEPLOY_CONTRACT, LIVE_DEMO, get_phase, launch_command, print_output, wait_for_phase
import sys


DEFAULT_CONTRACT_ADDRESS = "0x0542ae152b46ad771402d237ca8b6e217e1843d415411f4a312ceeb3be4e8d9e"

# Address of the smart-contract. Empty in the beginning, set by `deploy_contract()`
contract_addr = DEFAULT_CONTRACT_ADDRESS

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


def compile_contract():
    if COMPILE_CONTRACT:
        print("Compiling...")
        res = subprocess.run(['starknet-compile', 'contract.cairo',
                              '--output=contract_compiled.json', '--abi=contract_abi.json'], stdout=subprocess.PIPE)
        print_output(res)
        if res.returncode != 0:
            return res.returncode, 201
        print("Compilation done.")


def deploy_contract():
    global contract_addr
    if DEPLOY_CONTRACT:
        print("Deploying...")
        print("-- DEPLOY --\n")
        res = launch_command(['starknet', 'deploy', '--contract',
                              'contract_compiled.json', '--network', 'alpha'], True)
        if res.returncode != 0:
            print("Error while deploying: ", res.returncode)
            sys.exit(1)
        print("Deployment done.")
        out = res.stdout.decode('utf-8')

        # Dirty hack to extract contract address from process output.
        print(out.split('\n'))
        print(out.split('\n')[1])
        contract_addr = out.split('\n')[1][18:18+66]
        print('NEW CONTRACT ADDR', contract_addr)
    return "OK"


def initialize():
    print("Init...")
    if LIVE_DEMO:
        print('contract addr', contract_addr)
        print('serv pub key', str(serv_pub_key))
        print("-- INITIALIZE --\n")
        res = launch_command(['starknet',  'invoke', '--address', contract_addr,
                              '--abi', 'contract_abi.json', '--function', 'initialize', '--network', 'alpha', '--inputs', str(serv_pub_key)], True)
        if res.returncode != 0:
            return "Error executing initalize: exited with {}".format(res.returncode)
    print("Init done")
    # curr_phase = get_phase()
    # if curr_phase != 1:
    #     return "Error: did not properly increment phase"
    return "OK"


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


@ app.route('/api/get_contract_address', methods=['GET'])
def get_contract_address():
    return ({'contract_address': contract_addr})


# Submits the server key to the smart contract.
def key_submission():
    print("-- Submitting Key --")
    (r, s) = submit_key(serv_priv_key)
    if LIVE_DEMO:
        res = launch_command(['starknet', 'invoke', '--address', contract_addr, '--abi',
                              'contract_abi.json', '--function', '--network', 'alpha', 'submit_key', '--inputs', str(serv_priv_key), str(r), str(s)], True)
        if res.returncode != 0:
            return 'Error: submit key unsuccessful', 204
    return "Key submission OK"


@ app.route('/api/end_commit_phase', methods=['POST'])
def end_commit_phase():
    data = request.get_json()
    print(data)
    if 'message' not in data:
        return "Error: missing message!", 201
    message = data['message']

    # Dumb check to reduce the chance of a random guy ending the commit phase. Not secure, only used for POC presentation.
    if message != 'vitalik<3':
        return "Nice try feds!", 202

    print(serv_priv_key)
    (r, s) = end_commitment_phase(serv_priv_key)
    if (LIVE_DEMO):
        res = launch_command(['starknet', 'invoke', '--address', contract_addr, '--abi',
                              'contract_abi.json', '--function', 'end_commitment_phase', '--network', 'alpha', '--inputs', str(r), str(s)], True)
        if (res.returncode != 0):
            return 'Error: end_commit_phase unsuccessful', 203

    key_submission_result = key_submission()

    return key_submission_result


@ app.route('/api/end_voting_phase', methods=['POST'])
def end_voting_phase():
    data = request.get_json()
    print(data)
    if 'message' not in data:
        return "Error: missing message!", 201

    message = data['message']

    # Dumb check to reduce the chance of a random guy ending the commit phase. Not secure, only used for POC presentation.
    if message != 'vitalik<3':
        return "Nice try feds!", 202

    (r, s) = end_vote_phase(serv_priv_key)
    if LIVE_DEMO:
        res = launch_command(['starknet', 'invoke', '--address', contract_addr, '--abi',
                             'contract_abi.json', '--function', 'end_voting_phase', '--network', 'alpha', '--inputs', str(r), str(s)], True)
        if (res.returncode != 0):
            return 'Error: end voting phase unsuccessful', 203
    return "End voting phase OK"


@ app.route('/api/vote', methods=['POST'])
def vote():
    data = request.get_json()
    print(data)
    if 'public_key' not in data:
        return "Error: no public key provided", 206
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
        serv_priv_key, int(commit_token))
    if LIVE_DEMO:
        arguments = ['starknet', 'invoke', '--address', contract_addr, '--abi', 'contract_abi.json',
                     '--function', 'cast_vote', '--network', 'alpha', '--inputs', str(public_key), str(vote), str(hint_token_y), *serv_priv_key_decomposition]
        res = launch_command(arguments, True)
        if (res.returncode != 0):
            return 'Vote unsuccessful', 205
    return "Vote OK"


compile_contract()
deploy_contract()
msg = initialize()
if msg != "OK":
    print(msg)
    exit(1)

app.run(host="0.0.0.0", port=int(5000), use_reloader=False)
