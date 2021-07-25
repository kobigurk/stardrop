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

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

contract_addr = ""

# need to call node
db.makeDB()
(serv_priv_key, serv_pub_key) = generate_keypair()


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
    print("Deployment done.")
    out = deployment.stdout.decode('utf-8')

    # Dirty hack to extract contract address from process output.
    contract_addr = out.split('\n')[1][18:18+64]
    print(contract_addr)


def initialize():
    print("Init...")
    init = subprocess.run(['starknet',  'invoke', '--address', contract_addr,
                          '--abi', 'contract_abi.json', '--function', 'initialize', '--inputs', serv_pub_key, 1000, 2])
    if init.returncode != 0:
        return init.returncode, 201
    print("Init done")


# Easter egg
@ app.route('/', methods=['GET'])
def home():
    return "<h1>Wassu wassu wassu wassu wassu wassu wassuuuuuuuuupppppp!!!</h1>"


@ app.route('/api/sign_blinded_request', methods=['POST'])
def sign_blinded_request():
    if 'blinded_request' not in request.form:
        return 'Error: no blinded request provided', 201
    blinded_request = int(request.form['blinded_request'])
    (blinded_token, c, r) = sign_token(serv_priv_key, blinded_request)
    return ({'blinded_token': blinded_token, 'c': c, 'r': r})


@ app.route('/api/get_serv_public_key', methods=['GET'])
def get_serv_public_key():
    return ({'public_key': serv_pub_key})


# Submits the server key to the smart contract.
def key_submission():
    (r, s) = submit_key(serv_priv_key)
    ret = subprocess.run(['starknet', 'invoke', '--address', contract_addr, '--abi',
                         'contract_abi.json', '--function', 'submit_key', '--inputs', serv_priv_key, r, s])
    if (ret.returncode != 0):
        return 'Error: submit key unsuccessful', 204
    return "Key submission OK"


@ app.route('/api/end_commit_phase', methods=['POST'])
def end_commit_phase():
    if 'message' not in request.form:
        return "Error: missing message!", 201
    message = request.form['message']

    # Dumb check to reduce the chance of a random guy ending the commit phase. Not secure, only used for POC presentation.
    if message != 'vitalik<3':
        return "Nice try feds!", 202

    (r, s) = end_commitment_phase(serv_priv_key)
    ret = subprocess.run(['starknet', 'invoke', '--address', contract_addr, '--abi',
                          'contract_abi.json', '--function', 'end_commitment_phase', '--inputs', r, s])
    if (ret.returncode != 0):
        return 'Error: end_commit_phase unsuccessful', 203

    key_submission_result = key_submission()

    return key_submission_result


@ app.route('/api/end_voting_phase', methods=['POST'])
def end_voting_phase():
    if 'message' not in request.form:
        return "Error: missing message!", 201

    message = request.form['message']

    # Dumb check to reduce the chance of a random guy ending the commit phase. Not secure, only used for POC presentation.
    if message != 'vitalik<3':
        return "Nice try feds!", 202

    (r, s) = end_vote_phase(serv_priv_key)
    ret = subprocess.run(['starknet', 'invoke', '--address', contract_addr, '--abi',
                         'contract_abi.json', '--function', 'end_voting_phase', '--inputs', r, s])

    if (ret.returncode != 0):
        return 'Error: end voting phase unsuccessful', 203
    return "End voting phase OK"


@ app.route('/api/vote', methods=['POST'])
def vote():
    if 'public_key' not in request.form:
        return "Error: no public key provided", 201
    if 'commit_token' not in request.form:
        return "Error: no commit token provided", 202
    public_key = request.form['public_key']
    commit_token = request.form['commit_token']

    (hint_token_y, serv_priv_key_decomposition) = generate_vote_data(
        public_key, commit_token)
    arguments = ['starknet', 'invoke', '--address', contract_addr, '--abi', 'contract_abi.json',
                 '--function', 'cast_vote', '--inputs', serv_pub_key, hint_token_y] + serv_priv_key_decomposition
    ret = subprocess.run(arguments)
    if (ret.returncode != 0):
        return 'Vote unsuccessful', 203
    return "Vote OK"


app.run(host="0.0.0.0", port=int(5000))
