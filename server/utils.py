from re import sub
import subprocess
from sys import stdout
from time import sleep
import json
import requests

# whether to actually call and deploy starknet
INTERACT_WITH_STARKNET = True
DEPLOY_CONTRACT = True
COMPILE_CONTRACT = False
CHECK_POH = False
LOGGING = True


def print_output(subproc):
    print(subproc)
    if subproc.stdout:
        print(subproc.stdout.decode('utf-8'))
    if subproc.stderr:
        print(subproc.stderr.decode('utf-8'))


def wait_until_included(tx_id):
    if INTERACT_WITH_STARKNET:
        # 60 * 5s = 300 sec.
        for i in range(60):
            subproc = subprocess.run(
                ['starknet', 'tx_status', '--network', 'alpha', '--id', str(tx_id)], stdout=subprocess.PIPE)
            json_res = json.loads(subproc.stdout)
            print(json.dumps(json_res, indent=4, sort_keys=True))
            if "tx_failure_reason" in json_res:
                print("\n---TX FAILED---\n")
                return False
            elif json_res['tx_status'] == 'PENDING' or json_res['tx_status'] == 'ACCEPTED_ON_CHAIN':
                return True
            print("Waiting for tx {}... time elapsed: {}s".format(tx_id, i * 5))
            sleep(5)
        return False
    else:
        return True


def check_transaction_output(tx_id):
    if INTERACT_WITH_STARKNET:
        subproc = subprocess.run(
            ['starknet', 'tx_status', '--network', 'alpha', '--id', str(tx_id)], stdout=subprocess.PIPE)
        json_res = json.loads(subproc.stdout)
        print(json.dumps(json_res, indent=4, sort_keys=True))
    else:
        return True


def launch_command(args, last_tx_id):
    tx_id = -1
    if last_tx_id != -1:
        while tx_id < last_tx_id:
            subproc = subprocess.run(
                args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print_output(subproc)
            lines = subproc.stdout.decode('utf-8').split('\n')
            for line in lines:
                if "Transaction ID: " in line:
                    tx_id = int(line[len("Transaction ID: "):])
            # tx_id not found
            if tx_id == -1:
                subproc.returncode += 1
                return (tx_id, subproc)
    else:
        subproc = subprocess.run(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_output(subproc)
        lines = subproc.stdout.decode('utf-8').split('\n')
        for line in lines:
            if "Transaction ID: " in line:
                tx_id = int(line[len("Transaction ID: "):])

    return (tx_id, subproc)
