import sys

from starkware.crypto.signature.signature import (
    pedersen_hash, private_to_stark_key, get_random_private_key)


def generate_keypair():
    private_key = get_random_private_key() % 2**128
    public_key = private_to_stark_key(private_key)
    # print(f'Private key: {private_key}')
    # print(f'Public key: {public_key}')
    return (private_key, public_key)
