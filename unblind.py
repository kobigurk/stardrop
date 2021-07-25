import sys
from starkware.crypto.signature.signature import (
    pedersen_hash, private_to_stark_key, private_key_to_ec_point_on_stark_curve, get_random_private_key, verify, inv_mod_curve_size, EC_GEN, ALPHA, FIELD_PRIME, EC_ORDER, get_y_coordinate)

from starkware.crypto.signature.math_utils import (
    ECPoint, div_mod, ec_add, ec_double, ec_mult, is_quad_residue, sqrt_mod)


def unblind(blinded_token_in, blinding_factor, public_key_in, blinded_request, c, r):
    blinded_request = [blinded_request, get_y_coordinate(blinded_request)]

    found = False
    for i in range(4):
        public_key = [public_key_in, (1 if i == 0 or i == 1 else -1)
                      * get_y_coordinate(public_key_in) % FIELD_PRIME]
        blinded_token = [blinded_token_in, (1 if i == 0 or i == 2 else -1)
                         * get_y_coordinate(blinded_token_in) % FIELD_PRIME]
        t_hash = ec_mult(inv_mod_curve_size(blinding_factor),
                         blinded_token, ALPHA, FIELD_PRIME)[0]
        vG = ec_add(ec_mult(r, EC_GEN, ALPHA, FIELD_PRIME), ec_mult(
            c, public_key, ALPHA, FIELD_PRIME), FIELD_PRIME)
        vH = ec_add(ec_mult(r, blinded_request, ALPHA, FIELD_PRIME), ec_mult(
            c, blinded_token, ALPHA, FIELD_PRIME), FIELD_PRIME)
        c_prime = pedersen_hash(pedersen_hash(pedersen_hash(vG[0], vH[0]), pedersen_hash(
            public_key[0], blinded_token[0])), pedersen_hash(EC_GEN[0], blinded_request[0]))
        if (c - c_prime) % FIELD_PRIME == 0:
            found = True
            break

    assert found
    assert (c - c_prime) % FIELD_PRIME == 0
    #print(f'Blinded token: {blinded_token}')
    #print(f'Token: {t_hash}')
    #print(f'Blinding factor: {blinding_factor}')
    return (t_hash)
