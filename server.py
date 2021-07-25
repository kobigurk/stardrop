from claim_drop import claim_drop
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
    contract_addr = out.split('\n')[1][18:18+64]
    print(contract_addr)


def initialize():
    print("Init...")
    init = subprocess.run(['starknet',  'invoke', '--address', contract_addr,
                          '--abi', 'contract_abi.json', '--function', 'initialize', '--inputs', serv_pub_key, 1000, 2])
    if init.returncode != 0:
        return init.returncode, 201
    print("Init done")


@ app.route('/', methods=['GET'])
def home():
    return "<h1>Wassu wassu wassu wassu wassu wassu wassuuuuuuuuupppppp!!!</h1>"


@ app.route('/api/sign_blinded_request', methods=['POST'])
def sign_blinded_request():
    print(request.form)
    if 'blinded_request' not in request.form:
        return 'Error: no blinded request provided', 201
    blinded_request = int(request.form['blinded_request'])
    print("type")
    print(type(blinded_request))
    print(blinded_request)
    print("--\n\n\n")
    (blinded_token, c, r) = sign_token(serv_priv_key, blinded_request)
    return ({'blinded_token': blinded_token, 'c': c, 'r': r})


@ app.route('/api/get_serv_public_key', methods=['GET'])
def get_serv_public_key():
    return ({'public_key': serv_pub_key})


@ app.route('/api/end_commit_phase', methods=['POST'])
def end_commit_phase():
    (r, s) = end_commitment_phase(serv_priv_key)
    ret = subprocess.run(['starknet', 'invoke', '--address', contract_addr, '--abi',
                          'contract_abi.json', '--function', 'end_commitment_phase', '--inputs', r, s])
    if (ret.returncode != 0):
        return 'end_commit_phase subprocess ERROR', 201
    return 0


@ app.route('/api/submit_key', methods=['GET'])
def key_submission():
    (p_key, r, s) = submit_key(serv_priv_key)
    ret = subprocess.run(['starknet', 'invoke', '--address', contract_addr, '--abi',
                         'contract_abi.json', '--function', 'submit_key', '--inputs', p_key, r, s])
    if (ret.returncode != 0):
        return 'submit_key subprocess ERROR', 201
    return 0


@ app.route('/api/claim_drop', methods=['POST'])
def claiming_drop():
    if 'public_key' not in request.form:
        return "Error: no public key provided", 201
    if 'token' not in request.form:
        return "Error: no token provided", 202
    usr_public_key = request.form['public_key']
    token = request.form['token']
    (unknown_pblic_key, token_y, bin) = claim_drop(
        serv_priv_key, usr_public_key, token)
    ret = subprocess.run(['starknet', 'invoke', '--address', contract_addr, '--abi',
                         'contract_abi.json', '--function', 'submit_key', '--inputs', unknown_pblic_key, token_y, bin])
    if (ret.returncode != 0):
        return 'claim_drop subprocess ERROR', 203
    return 0


app.run(host="192.168.0.44")
