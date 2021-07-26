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
        if wait_until_included(tx_id) == False:
            return False
    return subproc
