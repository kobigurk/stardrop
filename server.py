from re import sub
from unblind import unblind
import flask
from generate_keypair import generate_keypair
from sign_token import sign_token
from blind import blind
from flask import request, jsonify
import subprocess
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


contract_addr = ""

# need to call node


def deploy_contract():
    print("Compiling...")
    compilation = subprocess.Popen(['starknet-compile', 'contract.cairo',
                                    '--output=contract_compiled.json', '--abi=contract_abi.json'])
    compilation.communicate()
    if compilation.returncode != 0:
        return compilation.returncode
    print("Compilation done.")

    print("Deploying...")
    deployment = subprocess.Popen(
        ['starknet', 'deploy', '--contract', 'contract_compiled.json', '--network', 'alpha'])
    (stdout, stderr) = deployment.communicate()
    stdout, stderr
    print("Deployment done.")
    out = stdout.decode('utf-8')
    print(out)


# CONTRACT_ADDR =$(starknet-compile contract.cairo
#                  - -output=contract_compiled.json
#                  - -abi=contract_abi.json & & starknet deploy - -contract contract_compiled.json - -network alpha

    # | grep address | awk '{print $3}' | tr - d \\.)
# deploy_contract()


# call set_database()
(serv_pub_key, serv_priv_key) = generate_keypair()


# remove this, use official fn
def try_vote(address: str) -> bool:
    return True


@ app.route('/', methods=['GET'])
def home():
    return "<h1>Wassu wassu wassu wassu wassu wassu wassuuuuuuuuupppppp!!!</h1>"


@ app.route('/api/generate_keys', methods=['GET'])
def generate_keys():
    (priv, pub) = generate_keypair()
    return jsonify([{'private_key': priv, 'public_key': pub}])


# @ app.route('/api/request_token', methods=['POST'])
def request_token(address):
    print("Request tokens")
#     if 'address' not in request.args:
    # return "Error: no address provided"

#     address = request.args['address']

    if try_vote(address) == False:
        return "Error: already voted or not in POH"

    (priv, pub) = generate_keypair()
    (blinded_request, blinded_factor) = blind(pub)

    (blinded_token, c, r) = sign_token(serv_priv_key, blinded_request)

    commit_token = unblind(blinded_token, blinded_factor,
                           pub, blinded_request, c, r)

    return (jsonify[{'commit_token': commit_token}])


request_token("0x123")


@ app.route('/api/commit', methods=['POST'])
def commit():
    return 'hi'


app.run(host="192.168.106.112")
