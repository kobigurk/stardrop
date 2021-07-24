import sys
from starkware.crypto.signature.signature import (
    pedersen_hash, private_to_stark_key, private_key_to_ec_point_on_stark_curve, get_random_private_key, verify, inv_mod_curve_size, EC_GEN, ALPHA, FIELD_PRIME, EC_ORDER, get_y_coordinate)

from starkware.crypto.signature.math_utils import (
    ECPoint, div_mod, ec_add, ec_double, ec_mult, is_quad_residue, sqrt_mod)


# returns (blinded_request, blinding_factor)
def blind(public_key):
    # public_key = int(sys.argv[1])
    t_hash = pedersen_hash(public_key, 0)
    t_hash = [t_hash, get_y_coordinate(t_hash)]
    blinding_factor = get_random_private_key()
    blinded_t_hash = ec_mult(blinding_factor, t_hash, ALPHA, FIELD_PRIME)[0]
    print(f'Public key: {public_key}')
    print(f'Request: {t_hash}')
    print(f'Blinded request: {blinded_t_hash}')
    print(f'Blinding factor: {blinding_factor}')
    return (blinded_t_hash, blinding_factor)
