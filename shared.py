from re import sub
import subprocess
from sys import stdout
from time import sleep
import json
import requests

# whether to actually call and deploy starknet
LIVE_DEMO = True
DEPLOY_CONTRACT = True
COMPILE_CONTRACT = False
CHECK_POH = False
LOGGING = True

SERV_URL = "http://192.168.106.112:5000"


def print_output(subproc):
    print(subproc)
    if subproc.stdout:
        print(subproc.stdout.decode('utf-8'))
    if subproc.stderr:
        print(subproc.stderr.decode('utf-8'))


def get_contract_address():
    contract_address_req = requests.get(SERV_URL + '/api/get_contract_address')
    req_json = contract_address_req.json()
    print(req_json)
    contract_address = req_json['contract_address']
    return contract_address


def get_phase(contract_address):
    if LIVE_DEMO:
        res = launch_command(['starknet',  'call', '--address', contract_address,
                              '--abi', 'contract_abi.json', '--network', 'alpha', '--function', 'get_phase'], False)
        if res.returncode != 0:
            return "Error executing starknet call: exited with {}".format(res.returncode), 201
        phase = int(res.stdout.decode('utf-8'))
    return phase


def wait_for_phase(expected_phase, contract_address):
    return
    for i in range(60):
        phase = get_phase(contract_address)
        if phase == expected_phase:
            return True
        print("Waiting for phase {}... time elapsed: {}s".format(
            expected_phase, i * 5))
        sleep(5)
    return False


def get_last_block():
    subproc = subprocess.run(
        ['starknet', 'get_block', '--network', 'alpha'], stdout=subprocess.PIPE)
    json_res = json.loads(subproc.stdout)
    block_id = int(json_res['block_id'])
    print("last block: ", json_res)
    print("last block id: ", block_id)
    return block_id


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
        # elif level == 'ACCEPTED':
        #     if json_res['tx_status'] == 'ACCEPTED_ON_CHAIN':
            # return True
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
            return subproc
        # if args[1] == 'deploy':
        #     if wait_until_included(tx_id, 'PENDING') == False:
            # return False
        if wait_until_included(tx_id, 'PENDING') == False:
            return False
    return subproc
