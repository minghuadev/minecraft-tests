

from cryptography.utils import int_from_bytes, int_to_bytes
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.exceptions import InvalidSignature


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


def save_to_hex_file(data_in, file_name):
    data_out = ""
    for x in data_in:
        data_out += "%02X" % x
    with open(file_name, "wb") as out_f:
        out_f.write(data_out.encode("ascii"))
        out_f.close()


