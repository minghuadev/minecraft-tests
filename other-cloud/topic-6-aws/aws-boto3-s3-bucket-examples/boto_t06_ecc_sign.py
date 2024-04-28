#
# boto3.amazonaws.com/v1/documentation/api/latest/
#       reference/services/kms/client/sign.html
#   the returned signature: When used with the ECDSA_SHA_256, ECDSA_SHA_384, 
#       or ECDSA_SHA_512 signing algorithms, this value is a DER-encoded object 
#       as defined by ANSI X9.62–2005 and RFC 3279 Section 2.2.3.
#
# boto3.amazonaws.com/v1/documentation/api/latest/
#       reference/services/kms/client/get_public_key.html
#   the returned is DER-encoded X.509 public key, also known as SubjectPublicKeyInfo (SPKI), 
#       as defined in RFC 5280.
#
# search offline verify aws ecc p256 signature python, 
# aws.amazon.com/blogs/security/
#       how-to-verify-aws-kms-signatures-in-decoupled-architectures-at-scale/
#
# also from boto_t05_kms02_encrypt.py

import boto3
from botocore.exceptions import ClientError
from pprint import pformat
import settings
import logging


logger = logging.getLogger(__name__)


class KeyEccNistP256:
    def __init__(self, kms_client, text_in=None):
        self.kms_client = kms_client
        self.text_in = text_in

    def sign_it(self, key_id):
        """
        Signs text by using the specified key.

        :param key_id: The ARN or ID of the key to use for encryption.
        :return: The encrypted version of the text.
        """
        text_in = self.text_in
        if text_in is None:
            text_in = input("Enter some text to encrypt: ")
        try:
            cipher_text = self.kms_client.sign(
                KeyId=key_id, 
                Message=text_in.encode(),
                MessageType='RAW',
                SigningAlgorithm="ECDSA_SHA_256"
            )["Signature"]
        except ClientError as err:
            logger.error(
                "Couldn't encrypt text. Here's why: %s",
                err.response["Error"]["Message"],
            )
        except Exception as err:
            logger.error(
                "Couldn't encrypt text. Here's why: %s",
                "Exception: %s" % str(err),
            )
        except:
            logger.error(
                "Couldn't encrypt text. Here's why: %s",
                "Exception: unknown"
            )
        else:
            print(f"Your signature length is: {len(cipher_text)}")
            print(f"Your signature is: {cipher_text}")
            return cipher_text

    def get_pub_key(self, key_id):
        """
        Gets the public key with a key.

        :param key_id: The ARN or ID of the key used to decrypt the data.
        """
        #answer = input("Ready to get the public key (y/n)? ")
        answer = "y"
        text = None # returned public key
        if answer.lower() == "y":
            try:
                pub_text = self.kms_client.get_public_key(
                    KeyId=key_id
                )
                text = b''
                if type(pub_text) is dict:
                    pubkeys = pub_text.keys()
                    if "PublicKey" in pubkeys:
                        text = pub_text["PublicKey"]
                        print("    ", "PublicKey: ", text)
                    else:
                        print("    ", "PublicKey: ", "known")
                    out_lines = pformat(pub_text, indent=2).splitlines()
                    for out_line in out_lines:
                        print("    ", out_line)
                else:
                    print("    ", "PublicKey type wrong")
            except ClientError as err:
                logger.error(
                    "Couldn't decrypt your ciphertext. Here's why: %s",
                    err.response["Error"]["Message"],
                )
            except Exception as err:
                logger.error(
                    "Couldn't decrypt your ciphertext. Here's why: %s",
                    "Exception: %s" % str(err),
                )
            except:
                logger.error(
                    "Couldn't decrypt your ciphertext. Here's why: %s",
                    "Exception: unknown"
                )
            else:
                print(f"Your public key length is {len(text)}")
                print(f"Your public key is {repr(text)}")
        else:
            print("Skipping decryption demo.")
        return text # the public key, or None, or b''


def key_signing(kms_client):
    logging.basicConfig(filename=None, level=logging.INFO, format="%(levelname)s: %(message)s")

    print("-" * 88)
    print("Welcome to the AWS Key Management Service (AWS KMS) key encryption demo.")
    print("-" * 88)

    #key_id = input("Enter a key ID or ARN to start the demo: ")
    key_id = settings.KEY_SIGN_ID
    if key_id == "":
        print("A key is required to run this demo.")
        return

    text_in = "welcome message everything looks ok"

    key_signs = KeyEccNistP256(kms_client, text_in=text_in)
    signature_text = key_signs.sign_it(key_id)
    print("-" * 88)
    if signature_text is not None:
        pub_key = key_signs.get_pub_key(key_id)
        print("-" * 88)
        aws_blog_verify(pub_der_key=pub_key, pub_signature=signature_text, 
                        pub_text=text_in)
        print("-" * 88)

    print("\nThanks for watching!")
    print("-" * 88)


def aws_blog_verify(pub_der_key=None, pub_signature=None, pub_text=None):
    import base64
    from hashlib import sha256

    import ecdsa # use pip install ecdsa, installed ecdsa-0.18.0
    from ecdsa.util import sigdecode_der

    """
    Input your JWT string for signature verification.
    You may use the sample JWT string and the following sample public key to run this code. 
    The signature in the sample JWT string below was produced using the private key paired 
    with the following sample public key.
    """
    #jwtStr = "eyJhbGciOiJFUzI1NiIsImtpZCI6ImFsaWFzL0VOVlNfVlRfU0lHTklOR19LRVkiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhd3MtZXhwb3N1cmUtbm90aWZpY2F0aW9ucy12ZXJpZmljYXRpb24tc2VydmVyIiwiZXhwIjoxNTk5NTg5NTM0LCJqdGkiOiJxMHg1N0lrRkMvSU9hdzAvNkpYVWhvaHFnV3RqZFVSaUNWMGpuVEpvR1BxTkNsbHdBWWhtTVJLUk1YOXUwb1I2bEtyTXNVSkdGZFJ6aCtncEJiakpCTWR4dVJBN3llYzEyWmE1SzJUMEFWWjZhMVdjNklYQ1ZlNGR6aHkyckJFbiIsImlhdCI6MTU5OTU4OTIzNCwiaXNzIjoiYXdzLWV4cG9zdXJlLW5vdGlmaWNhdGlvbnMtdmVyaWZpY2F0aW9uLXNlcnZlciIsInN1YiI6Im5lZ2F0aXZlLiJ9.MEYCIQCiLqsE2bxKdDi3NvX0mXqcHbvvDtI9zcCwPUHQiQutoQIhAJDhhCdRSlk_QYU_7_9X11yEcPzNHWF4qq2wRG66w7Lh"

    if pub_signature is not None and pub_text is not None and pub_der_key is not None:
        # read: https://github.com/tlsfuzzer/python-ecdsa
        # the section about "openssl compatibility"
        # we below call "verify()" in an openssl compatible form.
        signedStr = pub_text.encode()
        signature = pub_signature
        pass
    elif pub_signature is not None or pub_text is not None or pub_der_key is not None:
        print("Error: not all arguments are valid")
        pass
    else:
        # jwtStr1: sha256
        jwtStr1 = "eyJhbGciOiJFUzI1NiIsImtpZCI6ImFsaWFzL0VOVlNfVlRfU0lHTklOR19LRVkiLCJ0eXAiOiJKV1QifQ"
        # jwtStr2: ciphertext
        jwtStr2 = "eyJhdWQiOiJhd3MtZXhwb3N1cmUtbm90aWZpY2F0aW9ucy12ZXJpZmljYXRpb24tc2VydmVyIiwiZXhwI"
        jwtStr2 += "joxNTk5NTg5NTM0LCJqdGkiOiJxMHg1N0lrRkMvSU9hdzAvNkpYVWhvaHFnV3RqZFVSaUNWMGpuVEpvR1B"
        jwtStr2 += "xTkNsbHdBWWhtTVJLUk1YOXUwb1I2bEtyTXNVSkdGZFJ6aCtncEJiakpCTWR4dVJBN3llYzEyWmE1SzJUM"
        jwtStr2 += "EFWWjZhMVdjNklYQ1ZlNGR6aHkyckJFbiIsImlhdCI6MTU5OTU4OTIzNCwiaXNzIjoiYXdzLWV4cG9zdXJ"
        jwtStr2 += "lLW5vdGlmaWNhdGlvbnMtdmVyaWZpY2F0aW9uLXNlcnZlciIsInN1YiI6Im5lZ2F0aXZlLiJ9"
        # jwtStr3: signature
        jwtStr3 = "MEYCIQCi"
        jwtStr3 += "LqsE2bxKdDi3NvX0mXqcHbvvDtI9zcCwPUHQiQutoQIhAJDhhCdRSlk_QYU_7_9X11yEcPzNHWF4qq2wRG"
        jwtStr3 += "66w7Lh"
        jwtStr = jwtStr1 + "." + jwtStr2 + "." + jwtStr3
        #jwtStr = "<your-jwt-string>"
        jwtParts = jwtStr.split(".")

        # Compute a SHA-256 hash of the header and payload parts of the JWT string
        signedStr = ".".join(jwtParts[0:2]).encode(encoding="ASCII")
        signature = base64.urlsafe_b64decode(jwtParts[2])

    """    
    Decode the ECDSA public key copied from AWS KMS
    Sample public key --
    """
    """
    pubPemKey = ("-----BEGIN PUBLIC KEY-----\n"
        "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAErPPPHw8ilBwBNBhRZjyVOnKoHOri\n"
        "nS1ifFDScjQR4GRIcAzsTwlKjblMOcmxwy9TNOGrGnHTjw1XnIrBBhOPhg==\n"
        "-----END PUBLIC KEY-----")
    """
    #pubPemKey = "-----BEGIN PUBLIC KEY-----<your-key>-----END PUBLIC KEY-----"

    if pub_der_key is not None:
        verifyKey = ecdsa.VerifyingKey.from_der(pub_der_key)

    else:
        pubPemKey = ("-----BEGIN PUBLIC KEY-----\n"
            "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAErPPPHw8ilBwBNBhRZjyVOnKoHOri\n"
            "nS1ifFDScjQR4GRIcAzsTwlKjblMOcmxwy9TNOGrGnHTjw1XnIrBBhOPhg==\n"
            "-----END PUBLIC KEY-----")
        verifyKey = ecdsa.VerifyingKey.from_pem(pubPemKey)

    if verifyKey.verify(signature, signedStr, sha256, sigdecode=sigdecode_der):
        print ("Signature verification successful")
    else:    
        print ("Signature verification failed")


if __name__ == "__main__":
    try: 
        aws_blog_verify()
    except:
        logging.exception("Exception: unknown\n")
    else:
        logging.info("Blog verify ok\n")

    logging.info("Boto3 example ...")
    try:
        #key_encryption(boto3.client("kms"))
        kms_session = boto3.Session(
            aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
            aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
            region_name="us-east-2"
        )
        kms_client = kms_session.client("kms")
        key_signing(kms_client)

    except Exception as err:
        logging.exception("Something went wrong with the demo! " 
                          " Exception: " + str(err) + "\n")
    except:
        logging.exception("Something went wrong with the demo! "
                          " Exception: unknown\n")


