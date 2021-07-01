import sys
from starkware.crypto.signature.signature import (
    pedersen_hash, private_to_stark_key, private_key_to_ec_point_on_stark_curve, get_random_private_key, verify, inv_mod_curve_size, EC_GEN, ALPHA, FIELD_PRIME, EC_ORDER, get_y_coordinate)

from starkware.crypto.signature.math_utils import (
ECPoint, div_mod, ec_add, ec_double, ec_mult, is_quad_residue, sqrt_mod)

private_key = int(sys.argv[1])
public_key = private_to_stark_key(private_key)
public_key_computed = ec_mult(private_key, EC_GEN, ALPHA, FIELD_PRIME)[0]
print(f'public key: {public_key}')
print(f'public key computed: {public_key_computed}')
blinded_request = int(sys.argv[2])
blinded_request = [blinded_request, get_y_coordinate(blinded_request)]
blinded_token = ec_mult(private_key, blinded_request, ALPHA, FIELD_PRIME)[0]
#v = get_random_private_key()
v = 50
vG = ec_mult(v, EC_GEN, ALPHA, FIELD_PRIME)[0]
vH = ec_mult(v, blinded_request, ALPHA, FIELD_PRIME)[0]
c = pedersen_hash(pedersen_hash(pedersen_hash(vG, vH), pedersen_hash(public_key, blinded_token)), pedersen_hash(EC_GEN[0], blinded_request[0]))
r = (v - c*private_key) % EC_ORDER
print(f'Blinded request: {blinded_request}')
print(f'Blinded token: {blinded_token}')
print(f'Proof: {[c, r]}')