import sys

from starkware.crypto.signature.signature import (
    pedersen_hash, private_to_stark_key, private_key_to_ec_point_on_stark_curve, get_random_private_key, verify, inv_mod_curve_size, EC_GEN, ALPHA, FIELD_PRIME, EC_ORDER, sign, get_y_coordinate)
from starkware.crypto.signature.math_utils import (
ECPoint, div_mod, ec_add, ec_double, ec_mult, is_quad_residue, sqrt_mod)

key = int(sys.argv[1])
key_arr = list('{0:0128b}'.format(key))[::-1]
commitment_x = int(sys.argv[2])
commitment_y = get_y_coordinate(commitment_x)
t = ec_mult(key, [commitment_x, commitment_y], ALPHA, FIELD_PRIME)[0]

print(*[commitment_x, commitment_y, t, *key_arr], sep=' ')