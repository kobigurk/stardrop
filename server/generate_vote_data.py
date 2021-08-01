from starkware.crypto.signature.signature import (
    pedersen_hash, private_to_stark_key, private_key_to_ec_point_on_stark_curve, get_random_private_key, verify, inv_mod_curve_size, EC_GEN, ALPHA, FIELD_PRIME, EC_ORDER, sign, get_y_coordinate)
from starkware.crypto.signature.math_utils import (
    ECPoint, div_mod, ec_add, ec_double, ec_mult, is_quad_residue, sqrt_mod)


def generate_vote_data(key, token):
    serv_priv_key_bit_decomposition = list('{0:0128b}'.format(key))[::-1]
    #print(serv_priv_key_bit_decomposition)
    #print(len(serv_priv_key_bit_decomposition))
    token_y = get_y_coordinate(token)
    return (token_y, serv_priv_key_bit_decomposition)
