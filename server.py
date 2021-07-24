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
import re

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


contract_addr = ""

# need to call node
db.makeDB()

def deploy_contract():
    print("Compiling...")
    compilation = subprocess.run(['starknet-compile', 'contract.cairo',
                                  '--output=contract_compiled.json', '--abi=contract_abi.json'], stdout=subprocess.PIPE)
    print(compilation.stdout.decode('utf-8'))
    if compilation.returncode != 0:
        return compilation.returncode
    print("Compilation done.")

    print("Deploying...")
    deployment = subprocess.run(
        ['starknet', 'deploy', '--contract', 'contract_compiled.json', '--network', 'alpha'], stdout=subprocess.PIPE)
    print("Deployment done.")
    out = deployment.stdout.decode('utf-8')
    contract_addr = out.split('\n')[1][18:18+64]
    print(contract_addr)


# call set_database()
(serv_priv_key, serv_pub_key) = generate_keypair()

# remove this, use official fn



@ app.route('/', methods=['GET'])
def home():
    return "<h1>Wassu wassu wassu wassu wassu wassu wassuuuuuuuuupppppp!!!</h1>"


@ app.route('/api/generate_keys', methods=['GET'])
def generate_keys():
    (priv, pub) = generate_keypair()
    return jsonify([{'private_key': priv, 'public_key': pub}])
@ app.route('/api/end_commit_phase', methods=['GET'])
def end_commit_phase() :
    ret = subprocess.run(['starknet', 'invoke', '--address' ,contract_addr, '--abi', 'contract_abi.json', '--function', 'end_commitment_phase','--inputs', '1572514341211381639146744466808246693800547744347028176296700256447030933678', '1978481093464076802357781694214950813691007442586456313662641217350746463161'])
    if (ret.returncode != 0) :
        print('end_commit_phase subprocess ERROR')
    return 0

@ app.route('/api/request_token', methods=['POST'])
def request_token():
    if 'address' not in request.args:
        return "Error: no address provided"

    address = request.args['address']

    if db.try_vote(address) == False:
        return "Error: already voted or not in POH"

    (priv, pub) = generate_keypair()
    (blinded_request, blinded_factor) = blind(pub)

    (blinded_token, c, r) = sign_token(serv_priv_key, blinded_request)

    commit_token = unblind(blinded_token, blinded_factor,
                           serv_pub_key, blinded_request, c, r)

    return jsonify([{'commit_token': commit_token}])


@ app.route('/api/commit', methods=['POST'])
def commit():
    return 'hi'


app.run(host="192.168.106.112")
