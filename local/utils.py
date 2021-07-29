import os
from re import sub
import subprocess
from sys import stdout
from time import sleep
import json
import requests

INTERACT_WITH_STARKNET = False
LOGGING = True

SERVER_URL = os.environ.get('SERVER')


def print_output(subproc):
    print(subproc)
    if subproc.stdout:
        print(subproc.stdout.decode('utf-8'))
    if subproc.stderr:
        print(subproc.stderr.decode('utf-8'))


def get_contract_address():
    contract_address_req = requests.get(
        SERVER_URL + '/api/get_contract_address')
    req_json = contract_address_req.json()
    print(req_json)
    contract_address = req_json['contract_address']
    return contract_address


def wait_until_included(tx_id, level='Pending'):
    # 60 * 5s = 300 sec.
    for i in range(60):
        subproc = subprocess.run(
            ['starknet', 'tx_status', '--network', 'alpha', '--id', str(tx_id)], stdout=subprocess.PIPE)
        json_res = json.loads(subproc.stdout)
        print(json.dumps(json_res, indent=4, sort_keys=True))
        if "tx_failure_reason" in json_res:
            print("\n\n---TX FAILED---\n\n")
            return False
        elif json_res['tx_status'] == 'PENDING' or json_res['tx_status'] == 'ACCEPTED_ON_CHAIN':
            return True
        print("Waiting for tx {}... time elapsed: {}s".format(tx_id, i * 5))
        sleep(5)
    return False


def launch_command(args, should_wait_until_included):
    subproc = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print_output(subproc)
    if should_wait_until_included:
        lines = subproc.stdout.decode('utf-8').split('\n')
        tx_id = -1
        for line in lines:
            if "Transaction ID: " in line:
                tx_id = int(line[len("Transaction ID: "):])
        # tx_id not found
        if tx_id == -1:
            return (tx_id, subproc)
        if wait_until_included(tx_id, 'PENDING') == False:
            subproc.returncode = 1
            return (tx_id, subproc)
    return (tx_id, subproc)
