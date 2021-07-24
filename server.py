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

@ app.route('/api/generate_keys', methods=['GET'])
def generate_keys():
    (priv, pub) = generate_keypair()
    return jsonify([{'private_key': priv, 'public_key': pub}])


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

# call set_database()

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


@ app.route('/api/request_token', methods=['POST'])
def request_token():
    if 'address' not in request.args:
        return "Error: no address provided", 201

    address = request.args['address']

    if db.try_vote(address) == False:
        return "Error: already voted or not in POH", 202

    (priv, pub) = generate_keypair()
    (blinded_request, blinded_factor) = blind(pub)
    
    (blinded_token, c, r) = sign_token(serv_priv_key, blinded_request)

    commit_token = unblind(blinded_token, blinded_factor,
                           serv_pub_key, blinded_request, c, r)

    return jsonify([{'commit_token': commit_token}])

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
    (p_key ,r, s)  = submit_key(serv_priv_key)
    ret = subprocess.run(['starknet', 'invoke', '--address', contract_addr, '--abi', 'contract_abi.json', '--function', 'submit_key', '--inputs', p_key, r, s])
    if (ret.returncode != 0):
        return 'submit_key subprocess ERROR' , 201
    return 0

@ app.route('/api/claim_drop', methods=['GET'])
def claiming_drop():
    if 'public_key' not in request.args:
        return "Error: no public key provided", 201
    if 'token' not in request.args:
        return "Error: no token provided", 201
    usr_public_key = request.args['public_key']
    token = request.args['token']
    (unknown_pblic_key ,token_y, bin)  = claim_drop(serv_priv_key, usr_public_key, token)
    ret = subprocess.run(['starknet', 'invoke', '--address', contract_addr, '--abi', 'contract_abi.json', '--function', 'submit_key', '--inputs', unknown_pblic_key, token_y, bin])
    if (ret.returncode != 0):
        return 'claim_drop subprocess ERROR', 201
    return 0


app.run(host="192.168.106.112")
