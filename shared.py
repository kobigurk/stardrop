from re import sub
import subprocess

# whether to actually call and deploy starknet
LIVE_DEMO = True
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


# TODO: add bool to capture output, save txid, and 'await' for it
def launch_command(args):
    subproc = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print_output(subproc)
    return subproc.returncode
