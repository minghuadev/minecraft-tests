#!/usr/bin/env python
# common/common_crypto_utils.py

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.exceptions import InvalidSignature
from cryptography.utils import int_from_bytes, int_to_bytes
import os, time

# for attestation:
import base64

def pretty_print_hex(a, l=16, indent=''):
    """
    Format a list/bytes/bytearray object into a formatted ascii hex string
    """
    lines = []
    if type(a) is bytes or type(a) is bytearray:
        a = bytearray(a)
        for x in range(0, len(a), l):
            lines.append(indent + ' '.join(['{:02X}'.format(y) for y in a[x:x + l]]))
    else:
        lines.append(indent + ' ' + "<wrong-type-in-pretty_print_hex>")
    return '\n'.join(lines)

def convert_ec_pub_to_pem(raw_pub_key):
    """
    Convert to the key to PEM format. Expects bytes
    """
    public_key_der = bytearray.fromhex('3059301306072A8648CE3D020106082A8648CE3D03010703420004') + raw_pub_key
    public_key_b64 = base64.b64encode(public_key_der).decode('ascii')
    public_key_pem = (
        '-----BEGIN PUBLIC KEY-----\n'
        + '\n'.join(public_key_b64[i:i + 64] for i in range(0, len(public_key_b64), 64)) + '\n'
        + '-----END PUBLIC KEY-----'
    )
    return public_key_pem


def host_digest_message(message):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(message)
    digest = digest.finalize()
    return digest

def host_sign_digest(digest, key):
    signature = key.sign(digest, ec.ECDSA(utils.Prehashed(hashes.SHA256())))
    (r,s) = utils.decode_dss_signature(signature)
    signature = int_to_bytes(r, 32) + int_to_bytes(s, 32)
    return signature

def host_verify_digest(digest, signature, public_key_data):
    """
    Verify a signature using the host software
    """
    try:
        r = int_from_bytes(signature[0:32], byteorder='big', signed=False)
        s = int_from_bytes(signature[32:64], byteorder='big', signed=False)
        sig = utils.encode_dss_signature(r, s)

        public_key = ec.EllipticCurvePublicNumbers(
            curve=ec.SECP256R1(),
            x=int_from_bytes(public_key_data[0:32], byteorder='big'),
            y=int_from_bytes(public_key_data[32:64], byteorder='big'),
        ).public_key(default_backend())
        public_key.verify(sig, digest, ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        return True
    except InvalidSignature:
        return False

def date_stamp_u16():
    the_day = int( time.time() / 3600 / 24 ) # unix time
    if the_day >= 0xffff:
        return 0
    return the_day # value fits into uint16 size
