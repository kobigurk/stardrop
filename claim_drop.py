import sys

from starkware.crypto.signature.signature import (
    pedersen_hash, private_to_stark_key, private_key_to_ec_point_on_stark_curve, get_random_private_key, verify, inv_mod_curve_size, EC_GEN, ALPHA, FIELD_PRIME, EC_ORDER, sign, get_y_coordinate)
from starkware.crypto.signature.math_utils import (
    ECPoint, div_mod, ec_add, ec_double, ec_mult, is_quad_residue, sqrt_mod)


def claim_drop(private_key, key, token):
    public_key = private_to_stark_key(private_key)
    key_arr = list('{0:0128b}'.format(key))[::-1]
    token_y = get_y_coordinate(token)
    print(*[public_key, token_y, *key_arr], sep=' ')
    str_arr = str(key_arr).replace("[", "")
    str_arr = str_arr.replace("]", "")
    str_arr = str_arr.replace("\'", "")
    str_arr = str_arr.replace(",", "")
    return(public_key, token_y, str_arr)
