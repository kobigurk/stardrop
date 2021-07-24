import sys

from starkware.crypto.signature.signature import (
    pedersen_hash, private_to_stark_key, private_key_to_ec_point_on_stark_curve, get_random_private_key, verify, inv_mod_curve_size, EC_GEN, ALPHA, FIELD_PRIME, EC_ORDER, sign)
from starkware.crypto.signature.math_utils import (
    ECPoint, div_mod, ec_add, ec_double, ec_mult, is_quad_residue, sqrt_mod)


def commit(private_key, token):
    # private_key = int(sys.argv[1])
    public_key = private_to_stark_key(private_key)
    # token = int(sys.argv[2])
    (r, s) = sign(msg_hash=token, priv_key=private_key)

    print(f'Public key: {public_key}')
    print(f'Token: {token}')
    print(f'Signature: {(r, s)}')
