from generate_vote_data import generate_vote_data
import db
import flask
from sign_token import sign_token
from flask import request, jsonify
import subprocess
from flask_cors import CORS
from end_commitment_phase import end_commitment_phase
from end_vote_phase import end_vote_phase
from submit_key import sign_private_key
from generate_keypair import generate_keypair
from utils import CHECK_POH, COMPILE_CONTRACT, DEPLOY_CONTRACT, INTERACT_WITH_STARKNET, launch_command, print_output
import threading
import time
import datetime
import random
from datetime import timedelta, timezone


DEPLOYING_CONTRACT = 0
INITIALIZING_CONTRACT = 1
COMMIT_PHASE = 2
ENDING_COMMIT_PHASE = 3
SERVER_KEY_REVEAL = 4
VOTING_PHASE = 5
END_VOTING_PHASE = 6

VOTING_PHASE_LENGTH = 45
COMMIT_PHASE_LENGTH = 25

QUESTIONS = ['Should Carlos Matos be elected President of the United States?', 'Will you vote Yes?', 'Will you vote No?',
             'Is Dogecoin going to flip Ethereum?', 'Is Ethereum going to flip Bitcoin?', 'Are you Satoshi Nakamoto?']

# Address of the smart-contract. `None` in the beginning, set by `deploy_contract()`
contract_addr = None
serv_pub_key = None
serv_priv_key = None
state = None
question = random.choice(QUESTIONS)
total_yes = None
total_no = None
started_time = datetime.datetime.utcnow().timestamp()
previous_results = {'total_yes': total_yes,
                    'total_no': total_no, 'question': None}

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def compile_contract():
    if COMPILE_CONTRACT:
        print("Compiling...")
        res = launch_command(['starknet-compile', 'contract/contract.cairo',
                              '--output=contract/contract_compiled.json', '--abi=contract/contract_abi.json'], False)
        print_output(res)
        if res.returncode != 0:
            return "Failed to compile: returned {}".format(res.returncode)
        print("Compilation done.")
    return "OK"


def deploy_contract():
    global contract_addr
    if INTERACT_WITH_STARKNET and DEPLOY_CONTRACT:
        print("-- DEPLOY --\n")
        res = launch_command(['starknet', 'deploy', '--contract',
                              'contract/contract_compiled.json', '--network', 'alpha'], True)
        if res.returncode != 0:
            return "Error while deploying: {}".format(res.returncode)
        out = res.stdout.decode('utf-8')

        # Dirty hack to extract contract address from process output.
        print(out.split('\n'))
        print(out.split('\n')[1])
        contract_addr = out.split('\n')[1][18:18+66]

        print('NEW CONTRACT ADDR', contract_addr)
    return "OK"


def initialize():
    if INTERACT_WITH_STARKNET:
        print('contract addr', contract_addr)
        print('serv pub key', str(serv_pub_key))
        print("-- INITIALIZE --\n")

        res = launch_command(['starknet',  'invoke', '--address', contract_addr,
                              '--abi', 'contract/contract_abi.json', '--function', 'initialize', '--network', 'alpha', '--inputs', str(serv_pub_key)], True)

        if res.returncode != 0:
            return "Error executing initalize: exited with {}".format(res.returncode)
    return "OK"


@ app.route('/', methods=['GET'])
# Easter egg
def home():
    return "<h1>This is the voting server. It signs your commit_token, and then submits its key to smart-contract once the commit phase is done.</h1>"


def verify_sig(signature: str, message: str, poh_address: str) -> bool:
    # Utility function that calls a node script to verify if the `signature` is indeed `message` signed by `poh_address`.
    # Used to basically verify that the user is indeed the owner of poh_address.

    print("-- VERIFY SIG --\n")
    verif_process = launch_command(
        ['node', 'signGestion/get_signer_address.js', signature, message, poh_address], False)
    return verif_process.returncode == 0


@ app.route('/api/sign_blinded_request', methods=['POST'])
def sign_blinded_request():
    data = request.form
    if 'blinded_request' not in data:
        return 'Error: no blinded request provided', 201
    if 'poh_address' not in data:
        return 'Error: no POH address provided', 202
    if 'signature' not in data:
        return 'Error: no signature provided', 203

    blinded_request = int(data['blinded_request'])
    signature = data['signature']
    poh_address = data['poh_address']

    # Check that this the user is actually the owner of the POH address by verifying the signed message 'eip42'
    sig_is_valid = verify_sig(signature, 'eip42', poh_address)
    if not sig_is_valid:
        return "Error: invalid signature", 204

    (blinded_token, c, r) = sign_token(serv_priv_key, blinded_request)
    return ({'blinded_token': blinded_token, 'c': c, 'r': r})


@ app.route('/api/get_serv_public_key', methods=['GET'])
def get_serv_public_key():
    return ({'public_key': serv_pub_key})


@ app.route('/api/get_contract_address', methods=['GET'])
def get_contract_address():
    return ({'contract_address': contract_addr})


def key_submission():
    print("-- Submitting Key --")

    # Have the server sign its own private key.
    (r, s) = sign_private_key(serv_priv_key)

    if INTERACT_WITH_STARKNET:
        res = launch_command(['starknet', 'invoke', '--address', contract_addr, '--abi',
                              'contract/contract_abi.json', '--function', '--network', 'alpha', 'submit_key', '--inputs', str(serv_priv_key), str(r), str(s)], True)
        if res.returncode != 0:
            return 'Error: submit key unsuccessful', 204
    return "Key submission OK"


def end_commit_phase():
    print("-- Ending Commit Phase --")
    (r, s) = end_commitment_phase(serv_priv_key)

    if (INTERACT_WITH_STARKNET):
        res = launch_command(['starknet', 'invoke', '--address', contract_addr, '--abi',
                              'contract/contract_abi.json', '--function', 'end_commitment_phase', '--network', 'alpha', '--inputs', str(r), str(s)], True)
        if (res.returncode != 0):
            return 'Error: end_commit_phase unsuccessful', 203
    return "OK"


def end_voting_phase():
    print("-- End Voting Phase --")
    (r, s) = end_vote_phase(serv_priv_key)

    if INTERACT_WITH_STARKNET:
        res = launch_command(['starknet', 'invoke', '--address', contract_addr, '--abi',
                             'contract/contract_abi.json', '--function', 'end_voting_phase', '--network', 'alpha', '--inputs', str(r), str(s)], True)
        if (res.returncode != 0):
            return 'Error: end voting phase unsuccessful', 203
    return "End voting phase OK"


@ app.route('/api/vote', methods=['POST'])
def vote():
    # This function should be in `local.py` and local should ask the server to send priv key.
    data = request.get_json()
    print(data)
    if 'public_key' not in data:
        return "Error: no public key provided", 206
    if 'voting_token' not in data:
        return "Error: no voting token provided", 202
    if 'vote' not in data:
        return "Error: no vote provided", 203

    public_key = data['public_key']
    voting_token = data['voting_token']
    vote = data['vote']

    if vote == 'Yes':
        vote = 1
    elif vote == "No":
        vote = 0
    else:
        return "Error: invalid vote {}".format(vote), 204

    (hint_token_y, serv_priv_key_decomposition) = generate_vote_data(
        serv_priv_key, int(voting_token))
    if INTERACT_WITH_STARKNET:
        arguments = ['starknet', 'invoke', '--address', contract_addr, '--abi', 'contract/contract_abi.json',
                     '--function', 'cast_vote', '--network', 'alpha', '--inputs', str(public_key), str(vote), str(hint_token_y), *serv_priv_key_decomposition]
        res = launch_command(arguments, True)
        if (res.returncode != 0):
            return 'Vote unsuccessful', 205
    return "Vote OK"


def generate_human_list():
    if CHECK_POH:
        print("Generating human list...")
        humanlistProcess = subprocess.run(['node', 'getHumanList.js'])
        if humanlistProcess.returncode != 0:
            return "Failed to generate human list"
            re
        print("Generated human list!")
        print("Creating database")
        db.makeDB()
        print("Database successfully created")
    return "OK"


@ app.route('/api/get_state', methods=['GET'])
def get_state():

    if state == COMMIT_PHASE:
        current_time = datetime.datetime.utcnow().timestamp()
        end_time = started_time + COMMIT_PHASE_LENGTH + 1
        delay_to_callback = end_time - current_time
    elif state == VOTING_PHASE:
        current_time = datetime.datetime.utcnow().timestamp()
        end_time = started_time + COMMIT_PHASE_LENGTH + 1
        delay_to_callback = end_time - current_time
    else:
        delay_to_callback = 5

    return jsonify([{'phase': state, 'delay_to_callback': delay_to_callback, 'previous_results': previous_results, 'question': question}])


def update_results():
    global total_yes
    global total_no

    if INTERACT_WITH_STARKNET:
        print("-- GET RESULT --\n")
        res = launch_command(['starknet',  'call', '--address', contract_addr,
                              '--abi', 'contract/contract_abi.json', '--network', 'alpha', '--function', 'get_result'], False)
        if res.returncode != 0:
            return "Error executing starknet call: exited with {}".format(res.returncode), 201
        (total_yes, total_no) = res.stdout.decode('utf-8').split(' ')
        total_yes = int(total_yes)
        total_no = int(total_no)


result = generate_human_list()
if result != "OK":
    print(result)
    exit(1)

result = compile_contract()
if result != "OK":
    print(result)
    exit(1)


threading.Thread(target=app.run, kwargs={
    'host': "0.0.0.0", 'port': int(5000), 'use_reloader': False}).start()

while (42):
    (serv_priv_key, serv_pub_key) = generate_keypair()
    print("Server keypair succesfully created: private: {}, public: {}".format(
        serv_priv_key, serv_pub_key))

    state = DEPLOYING_CONTRACT
    started_time = datetime.datetime.utcnow().timestamp()
    result = deploy_contract()
    if result != "OK":
        print(result)
        exit(1)

    state = INITIALIZING_CONTRACT
    started_time = datetime.datetime.utcnow().timestamp()
    msg = initialize()
    if msg != "OK":
        print(msg)
        exit(1)

    state = COMMIT_PHASE
    started_time = datetime.datetime.utcnow().timestamp()
    print("-- COMMIT PHASE --")
    time.sleep(COMMIT_PHASE_LENGTH)

    state = ENDING_COMMIT_PHASE
    started_time = datetime.datetime.utcnow().timestamp()
    end_commit_phase()

    state = SERVER_KEY_REVEAL
    started_time = datetime.datetime.utcnow().timestamp()
    key_submission()

    state = VOTING_PHASE
    started_time = datetime.datetime.utcnow().timestamp()
    print("-- Voting Phase --")
    time.sleep(VOTING_PHASE_LENGTH)

    state = END_VOTING_PHASE
    end_voting_phase()
    update_results()

    previous_results.update(
        {'total_no': total_no, 'total_yes': total_yes, 'question': question})
    question = random.choice(QUESTIONS)

    state = DEPLOYING_CONTRACT
