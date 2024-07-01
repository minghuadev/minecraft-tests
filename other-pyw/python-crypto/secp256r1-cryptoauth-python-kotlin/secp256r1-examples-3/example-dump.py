

from service.service_common_ecdh import (host_ecdh_create_key,
                                         host_ecdh_create_shared)
from common.common_crypto_utils import (host_digest_message,
                                        host_sign_digest,
                                        host_verify_digest)
from service.example_utils import convert_sig_rs_to_der, save_to_hex_file

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import (PrivateFormat,
                                                          NoEncryption,
                                                          load_pem_private_key,
                                                          load_der_private_key)
import base64
from cryptography.fernet import Fernet
import os


key_prv_filename = "tmp_k_prv.private"
key_pub_filename = "tmp_k_pub.pub"

if (not os.path.isfile(key_prv_filename) or
        not os.path.isfile(key_pub_filename)):
    kpair = host_ecdh_create_key()
    print(kpair)

    prv_k = kpair[0]
    pub_k = kpair[1]

    # both Encoding.PEM and Encoding.DER works. PEM size 241, DER 138.
    prv_k_pem = prv_k.private_bytes(encoding=Encoding.DER,
                                    format=PrivateFormat.PKCS8,
                                    encryption_algorithm=NoEncryption())
    # write key:
    with open(key_prv_filename, "wb") as f:
        f.write(prv_k_pem)
        f.close()  # pem
    with open(key_pub_filename, "wb") as f:
        f.write(pub_k)  # bytes
        f.close()
    save_to_hex_file(prv_k_pem, key_prv_filename + ".hex")
    save_to_hex_file(pub_k, key_pub_filename + ".hex")
else:
    prv_k, pub_k = None, None
    with open(key_pub_filename, "rb") as f:
        pub_k = f.read(65) # attempt read one byte more than 64
        f.close()
        if type(pub_k) is not bytes or len(pub_k) != 64:
            pub_k = None
    with open(key_prv_filename, "rb") as f:
        key_prv_pem = f.read(512)
        f.close()
        #prv_k = load_pem_private_key(key_prv_pem, password=None)
        prv_k = load_der_private_key(key_prv_pem, password=None)

# from service_common.py, sign_session():
msg = bytearray(b'this is an input example message')
dgst = host_digest_message(msg) # bytes of 32
sig = host_sign_digest(dgst, prv_k) # bytes of 64

sig_der = convert_sig_rs_to_der(sig)
save_to_hex_file(sig_der, "tmp_out_sig_hex")

# from service_common.py, verify_device_cert():
verified = host_verify_digest(dgst, sig, pub_k)
print("verified: ", verified)

# encryption decryption:
shared_key = host_ecdh_create_shared(prv_k, pub_k) # bytes of 32
print("shared_key: ", shared_key)
save_to_hex_file(shared_key, "tmp_out_shared_key_hex")

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

def host_aes_encrypt_plain(shared_secret, msg): # from host_ecdh_kdf_encrypt()

    message = bytes(msg)

    encryption_key = shared_secret[:16]
    # inside: AES.block_size == 128
    # current_time = int(time.time())
    # self._signing_key = key[:16]
    # self._encryption_key = key[16:]
    # iv = os.urandom(16)
    iv = b'abcd1234defg5678'

    from cryptography.hazmat.primitives import hashes, padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import _get_backend

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    backend = _get_backend(None)
    padded_data = padder.update(message) + padder.finalize()
    encryptor = Cipher(
        algorithms.AES(encryption_key), modes.CBC(iv), backend
    ).encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext

cipher_txt = host_aes_encrypt_plain(shared_key, msg)
print("cipher_txt: ", cipher_txt)
save_to_hex_file(cipher_txt, "tmp_out_cipher_txt")

