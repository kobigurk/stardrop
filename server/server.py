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
import logging


DEPLOYING_CONTRACT = 0
INITIALIZING_CONTRACT = 1
COMMIT_PHASE = 2
ENDING_COMMIT_PHASE = 3
SERVER_KEY_REVEAL = 4
VOTING_PHASE = 5
END_VOTING_PHASE = 6
##### ERRORS #########
NET_CALL_ERR = 201
NO_PUB_KEY_ERR = 202
END_COMMIT_ERR = 203
END_VOTE_ERR = 204
KEY_SUB_ERR = 205
NO_VOTE_TOKEN_ERR = 206
NO_VOTE_ERR = 207
INVALID_VOTE_ERR = 208
UNSUCCESSFUL_VOTE_ERR = 209
##################################
LOG_FORMAT = "%(levelname)s %(asctime)s \"%(message)s \""

if INTERACT_WITH_STARKNET:
    VOTING_PHASE_LENGTH = 45
    COMMIT_PHASE_LENGTH = 25
else:
    VOTING_PHASE_LENGTH = 15
    COMMIT_PHASE_LENGTH = 15

QUESTIONS = ['Should Carlos Matos be elected President of the United States?', 'Will you vote Yes?', 'Will you vote No?',
             'Is Dogecoin going to flip Ethereum?', 'Is Ethereum going to flip Bitcoin?', 'Are you Satoshi Nakamoto?']

# Address of the smart-contract. `None` in the beginning, set by `deploy_contract()`
print("Logging file == " + logging.__file__)
logging.basicConfig(filename = "./route.log", level = logging.INFO, format = LOG_FORMAT, filemode = 'w')
logger = logging.getLogger()
logging.info("Starting Server")
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
        logging.info("Compiling...")
        (_, res) = launch_command(['starknet-compile', 'contract/contract.cairo',
                              '--output=contract/contract_compiled.json', '--abi=contract/contract_abi.json'], False)
        logging.debug(res)
        print_output(res)
        if res.returncode != 0:
            logging.critical("Failed to compile: returned {}".format(res.returncode))
            return "Check route.log"
        logging.info("Compilation done.")
    return "OK"


def deploy_contract():
    global contract_addr
    if INTERACT_WITH_STARKNET and DEPLOY_CONTRACT:
        logging.info("-- DEPLOY --")
        (_, res) = launch_command(['starknet', 'deploy', '--contract',
                              'contract/contract_compiled.json', '--network', 'alpha'], True)
        if res.returncode != 0:
            logging.critical("Error while deploying: {}".format(res.returncode))
            return "Check route.log"
        out = res.stdout.decode('utf-8')

        # Dirty hack to extract contract address from process output.
        logging.debug(out.split('\n'))
        logging.debug(out.split('\n')[1])
        contract_addr = out.split('\n')[1][18:18+66]

        logging.info('NEW CONTRACT ADDR', contract_addr)
    else:
        time.sleep(8)
    return "OK"


def initialize():
    if INTERACT_WITH_STARKNET:
        logging.info('Contract addr', contract_addr)
        logging.info('Serv public_key', str(serv_pub_key))
        logging.info("-- INITIALIZE --\n")

        (_, res) = launch_command(['starknet',  'invoke', '--address', contract_addr,
                              '--abi', 'contract/contract_abi.json', '--function', 'initialize', '--network', 'alpha', '--inputs', str(serv_pub_key)], True)

        if res.returncode != 0:
            logging.critical("Error executing initalize: exited with {}".format(res.returncode))
            return "Check route.log"
    else:
        time.sleep(8)
    logging.info("Initialize finished")
    return "OK"


@ app.route('/', methods=['GET'])
# Easter egg
def home():
    return "<h1>This is the voting server. It signs your commit_token, and then submits its key to smart-contract once the commit phase is done.</h1>"


def verify_sig(signature: str, message: str, poh_address: str) -> bool:
    # Utility function that calls a node script to verify if the `signature` is indeed `message` signed by `poh_address`.
    # Used to basically verify that the user is indeed the owner of poh_address.

    logging.info("-- VERIFY SIG --\n")
    (_, verif_process) = launch_command(
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
    if 'force_commit' not in data:
        return 'Error: no force_commit provided', 204

    blinded_request = int(data['blinded_request'])
    signature = data['signature']
    poh_address = data['poh_address']
    force_commit = data['force_commit']

    # Check that user is in the POH list
    if force_commit != "Yes" and not db.try_vote(poh_address):
        return "Error: user not in poh_address", 205

    # Check that this the user is actually the owner of the POH address by verifying the signed message 'eip42'
    sig_is_valid = verify_sig(signature, 'eip42', poh_address)
    if not sig_is_valid:
        return "Error: invalid signature", 206

    (blinded_token, c, r) = sign_token(serv_priv_key, blinded_request)
    logging.debug(f'Blinded token: {blinded_token}')
    logging.debug(f'Proof: {[c, r]}')
    return ({'blinded_token': blinded_token, 'c': c, 'r': r})


@ app.route('/api/get_serv_public_key', methods=['GET'])
def get_serv_public_key():
    return ({'public_key': serv_pub_key})


@ app.route('/api/get_contract_address', methods=['GET'])
def get_contract_address():
    return ({'contract_address': contract_addr})


def key_submission():
    logging.info("-- Submitting Key --")

    # Have the server sign its own private key.
    (r, s) = sign_private_key(serv_priv_key)
    logging.debug(f'Signature: {(r, s)}')
    if INTERACT_WITH_STARKNET:
        (_, res) = launch_command(['starknet', 'invoke', '--address', contract_addr, '--abi',
                              'contract/contract_abi.json', '--function', '--network', 'alpha', 'submit_key', '--inputs', str(serv_priv_key), str(r), str(s)], True)
        if res.returncode != 0:
            logging.critical('Error' + KEY_SUB_ERR + ': submit key unsuccessful')
            return 'Error: submit key unsuccessful', KEY_SUB_ERR
    else:
        time.sleep(8)
    logging.info("Key submission OK")
    return "OK"


def end_commit_phase():
    logging.info("-- Ending Commit Phase --")
    (r, s) = end_commitment_phase(serv_priv_key)
    logging.debug(f'Signature: {(r, s)}')
    if (INTERACT_WITH_STARKNET):
        (_, res) = launch_command(['starknet', 'invoke', '--address', contract_addr, '--abi',
                              'contract/contract_abi.json', '--function', 'end_commitment_phase', '--network', 'alpha', '--inputs', str(r), str(s)], True)
        if (res.returncode != 0):
            logging.critical("Error" + END_COMMIT_ERR + ": end_commit_phase unsuccessful")
            return 'Error: end_commit_phase unsuccessful', END_COMMIT_ERR
    else:
        time.sleep(8)
    logging.info("End_commit_phase OK")
    return "OK"


def end_voting_phase():
    logging.info("-- End Voting Phase --")
    (r, s) = end_vote_phase(serv_priv_key)
    logging.debug(f'Signature: {(r, s)}')
    if INTERACT_WITH_STARKNET:
        (_, res) = launch_command(['starknet', 'invoke', '--address', contract_addr, '--abi',
                             'contract/contract_abi.json', '--function', 'end_voting_phase', '--network', 'alpha', '--inputs', str(r), str(s)], True)
        if (res.returncode != 0):
            logging.critical("Error" + END_VOTE_ERR + ": end voting phase unsuccessful")
            return 'Error: end voting phase unsuccessful', END_VOTE_ERR
    else:
        time.sleep(8)
    logging.info("End voting phase OK")
    return "End voting phase OK"


@ app.route('/api/vote', methods=['POST'])
def vote():
    # This function should be in `local.py` and local should ask the server to send priv key.
    data = request.get_json()
    logging.debug(data)
    if 'public_key' not in data:
        logging.error("Error" + NO_PUB_KEY_ERR + ": no public key provided")
        return "Error: no public key provided", NO_PUB_KEY_ERR
    if 'voting_token' not in data:
        logging.error("Error" + NO_VOTE_TOKEN_ERR + ": no voting token provided")
        return "Error: no voting token provided", NO_VOTE_TOKEN_ERR
    if 'vote' not in data:
        logging.error("Error" + NO_VOTE_ERR + ": no vote provided")
        return "Error: no vote provided", NO_VOTE_ERR

    public_key = data['public_key']
    voting_token = data['voting_token']
    vote = data['vote']

    if vote == 'Yes':
        vote = 1
    elif vote == "No":
        vote = 0
    else:
        logging.error("Error" + INVALID_VOTE_ERR + ": invalid vote {}".format(vote))
        return "Error: invalid vote {}".format(vote), INVALID_VOTE_ERR

    (hint_token_y, serv_priv_key_decomposition) = generate_vote_data(
        serv_priv_key, int(voting_token))
    logging.debug("Hint token y :" + hint_token_y + "Serv. priv. key decomposition" + serv_priv_key_decomposition + 'len =' + len(serv_priv_key_decomposition))
    if INTERACT_WITH_STARKNET:
        arguments = ['starknet', 'invoke', '--address', contract_addr, '--abi', 'contract/contract_abi.json',
                     '--function', 'cast_vote', '--network', 'alpha', '--inputs', str(public_key), str(vote), str(hint_token_y), *serv_priv_key_decomposition]
        (_, res) = launch_command(arguments, True)
        if (res.returncode != 0):
            logging.error("Error" + UNSUCCESSFUL_VOTE_ERR + ": unsuccessful vote")
            return 'Vote unsuccessful', UNSUCCESSFUL_VOTE_ERR
    else:
        time.sleep(8)
    logging.info("Vote OK")
    return "Vote OK"


def generate_human_list():
    if CHECK_POH:
        logging.info("Generating human list...")
        humanlistProcess = subprocess.run(['node', 'getHumanList.js'])
        if humanlistProcess.returncode != 0:
            logging.critical("Failed to generate Human list")
            return "Failed to generate human list"
        logging.info("Generated human list!")
        logging.info("Creating database")
        db.makeDB()
        logging.info("Database successfully created")
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
        logging.info("-- GET RESULT --\n")
        (_, res) = launch_command(['starknet',  'call', '--address', contract_addr,
                              '--abi', 'contract/contract_abi.json', '--network', 'alpha', '--function', 'get_result'], False)
        if res.returncode != 0:
            logging.critical("Error" + NET_CALL_ERR + ": executing starknet call: exited with {}".format(res.returncode))
            return "Error executing starknet call: exited with {}".format(res.returncode), NET_CALL_ERR
        (total_yes, total_no) = res.stdout.decode('utf-8').split(' ')
        total_yes = int(total_yes)
        total_no = int(total_no)
    else:
        total_yes = random.randint()
        total_no = random.randint()


result = generate_human_list()
if result != "OK":
    #logging.error("Generate human list result --> result")
    exit(1)

result = compile_contract()
if result != "OK":
    #logging.error("Compiling contract result --> result")
    exit(1)


threading.Thread(target=app.run, kwargs={
    'host': "0.0.0.0", 'port': int(5000), 'use_reloader': False}).start()

while (42):
    (serv_priv_key, serv_pub_key) = generate_keypair()
    logging.info("Server keypair succesfully created: private: {}, public: {}".format(
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
    logging.info("-- COMMIT PHASE --")
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
    logging.info("-- Voting Phase --")
    print("-- Voting Phase --")
    time.sleep(VOTING_PHASE_LENGTH)

    state = END_VOTING_PHASE
    end_voting_phase()
    update_results()

    previous_results.update(
        {'total_no': total_no, 'total_yes': total_yes, 'question': question})
    question = random.choice(QUESTIONS)

    state = DEPLOYING_CONTRACT
    logging.info("Everything went well")
