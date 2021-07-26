from starkware.crypto.signature.signature import (
    pedersen_hash, private_to_stark_key, private_key_to_ec_point_on_stark_curve, get_random_private_key, verify, inv_mod_curve_size, EC_GEN, ALPHA, FIELD_PRIME, EC_ORDER, get_y_coordinate)

from starkware.crypto.signature.math_utils import (
    ECPoint, div_mod, ec_add, ec_double, ec_mult, is_quad_residue, sqrt_mod)


def blind(public_key):
    t_hash = pedersen_hash(public_key, 0)
    t_hash = [t_hash, get_y_coordinate(t_hash)]
    blinding_factor = get_random_private_key()
    blinded_t_hash = ec_mult(blinding_factor, t_hash, ALPHA, FIELD_PRIME)[0]
    return (t_hash[0], blinded_t_hash, blinding_factor)
