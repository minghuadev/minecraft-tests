#!/usr/bin/env python
# service/service_common_ecdh.py

# ===========================================================================
# (c) 2015-2019 Microchip Technology Inc. and its subsidiaries.
#
# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.
#
# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
# PARTICULAR PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT,
# SPECIAL, PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE
# OF ANY KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF
# MICROCHIP HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE
# FORESEEABLE. TO THE FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL
# LIABILITY ON ALL CLAIMS IN ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED
# THE AMOUNT OF FEES, IF ANY, THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR
# THIS SOFTWARE.

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.utils import int_from_bytes, int_to_bytes
import os, time

import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

# for attestation:
from textwrap import TextWrapper
from hashlib import sha256
import struct, copy

# for session
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# common_crypto
from common.common_crypto_utils import pretty_print_hex, convert_ec_pub_to_pem
from common.common_crypto_utils import host_digest_message, host_sign_digest, host_verify_digest

# ===========================================================================

def host_ecdh_create_key():
    # Create a host private key
    host_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

    # Convert host's public key into ATECCx08 format
    host_pub = host_key.public_key().public_bytes(encoding=Encoding.X962,
                                                  format=PublicFormat.UncompressedPoint)[1:]
    return host_key, host_pub

def host_ecdh_create_shared(host_key, device_pub):
    # Convert device public key to a cryptography public key object
    device_pub = ec.EllipticCurvePublicNumbers(
        curve=ec.SECP256R1(),
        x=int_from_bytes(device_pub[0:32], byteorder='big'),
        y=int_from_bytes(device_pub[32:64], byteorder='big'),
    ).public_key(default_backend())

    # Perform the host side ECDH computation
    host_shared = host_key.exchange(ec.ECDH(), device_pub)
    return host_shared

def host_ecdh_kdf_encrypt(shared_secret):
    password_provided = "password"  # This is input in the form of a string
    password = password_provided.encode()  # Convert to type bytes
    salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    salt += shared_secret  # the ecdh shared secret key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once

    message_clear_part = shared_secret[:3] + shared_secret[-3:]  # 3-head + 3-tail
    message = bytes(message_clear_part)

    f = Fernet(key)
    encrypted = f.encrypt(message)  # Encrypt the bytes. The returning object is of type bytes

    # f = Fernet(key)
    # try:
    #     decrypted = f.decrypt(encrypted)  # Decrypt the bytes. The returning object is of type bytes
    #     print("Valid key - successfuly decrypted")
    #     if decrypted == message:
    #         print("Ok: Messages match")
    #     else:
    #         print("Error: Messages mis-match")
    # except InvalidToken as e:
    #     print("Invalid key - unsuccessfully decrypted", e)

    return message_clear_part + encrypted

def host_ecdh_kdf_decrypt_verify(encrypted_message, shared_secret):
    password_provided = "password"  # This is input in the form of a string
    password = password_provided.encode()  # Convert to type bytes
    salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    salt += shared_secret  # the ecdh shared secret key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once

    message_clear_part_ref = shared_secret[:3] + shared_secret[-3:]  # 3-head + 3-tail
    message_clear_part = encrypted_message[:6]
    if message_clear_part != message_clear_part_ref:
        print("KDF verify failed to extract the message clear part")
        return False

    message = encrypted_message[6:]
    f = Fernet(key)
    try:
        decrypted = f.decrypt( bytes(message) )  # Decrypt the bytes. The returning object is of type bytes
        print("Valid key - successfuly decrypted")
        if decrypted == message_clear_part:
            print("Ok: Messages match")
            return True
        else:
            print("Error: Messages mis-match")
    except InvalidToken as e:
        print("Invalid key - unsuccessfully decrypted", e)

    return False

# ===========================================================================

