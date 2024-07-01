

from service.service_common_ecdh import (host_ecdh_create_key,
                                         host_ecdh_create_shared)
from common.common_crypto_utils import (host_digest_message,
                                        host_sign_digest,
                                        host_verify_digest)

from cryptography.utils import int_from_bytes, int_to_bytes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
from cryptography.fernet import Fernet


kpair = host_ecdh_create_key()
print(kpair)

prv_k = kpair[0]
pub_k = kpair[1]

# from service_common.py, sign_session():
msg = bytearray(b'this is an input example message')
dgst = host_digest_message(msg) # bytes of 32
sig = host_sign_digest(dgst, prv_k) # bytes of 64

def convert_sig_rs_to_der(sig_rs):
    sig_der = None
    try:
        r = int_from_bytes(sig_rs[0:32], byteorder='big', signed=False)
        s = int_from_bytes(sig_rs[32:64], byteorder='big', signed=False)
        sig_der = utils.encode_dss_signature(r, s) # bytes of 70, 71, 72
    except InvalidSignature:
        pass
    except:
        pass
    return sig_der

def convert_sig_der_to_rs(sig_der):
    sig_rs = None
    try:
        (r, s) = utils.decode_dss_signature(sig_der)
        sig_rs = int_to_bytes(r, 32) + int_to_bytes(s, 32)
    except InvalidSignature:
        pass
    except:
        pass
    return sig_rs

sig_der = convert_sig_rs_to_der(sig)

# from service_common.py, verify_device_cert():
v = host_verify_digest(dgst, sig, pub_k)
print("v: ", v)

# encryption decryption:
shared_key = host_ecdh_create_shared(prv_k, pub_k) # bytes of 32
print("shared_key: ", shared_key)

def host_aes_encrypt(shared_secret, msg): # from host_ecdh_kdf_encrypt()
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
    # inside: AES.block_size == 128
    # current_time = int(time.time())
    # self._signing_key = key[:16]
    # self._encryption_key = key[16:]
    # iv = os.urandom(16)
    # padder = padding.PKCS7(algorithms.AES.block_size).padder()
    # padded_data = padder.update(data) + padder.finalize()
    # encryptor = Cipher(
    #     algorithms.AES(self._encryption_key), modes.CBC(iv), self._backend
    # ).encryptor()
    # ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    #
    # basic_parts = (
    #         b"\x80" + struct.pack(">Q", current_time) + iv + ciphertext
    # )
    #
    # h = HMAC(self._signing_key, hashes.SHA256(), backend=self._backend)
    # h.update(basic_parts)
    # hmac = h.finalize()
    # return base64.urlsafe_b64encode(basic_parts + hmac)

    # decryption snippet:
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
    # inside:
    # (timestamp,) = struct.unpack(">Q", data[1:9])
    # h = HMAC(self._signing_key, hashes.SHA256(), backend=self._backend)
    # h.update(data[:-32])
    # h.verify(data[-32:])
    # iv = data[9:25]
    # ciphertext = data[25:-32]
    # decryptor = Cipher(
    #     algorithms.AES(self._encryption_key), modes.CBC(iv), self._backend
    # ).decryptor()
    # plaintext_padded = decryptor.update(ciphertext)
    # try:
    #     plaintext_padded += decryptor.finalize()
    # except ValueError:
    #     raise InvalidToken
    # unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    #
    # unpadded = unpadder.update(plaintext_padded)
    # try:
    #     unpadded += unpadder.finalize()

    return message_clear_part + encrypted

cipher_txt = host_aes_encrypt(shared_key, msg)
print("cipher_txt: ", cipher_txt)

