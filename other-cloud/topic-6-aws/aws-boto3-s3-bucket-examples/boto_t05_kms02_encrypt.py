#
# docs.aws.amazon.com/code-library/latest/ug/python_3_kms_code_examples.html

import boto3
from botocore.exceptions import ClientError
import settings
import logging


logger = logging.getLogger(__name__)


class KeyEncrypt:
    def __init__(self, kms_client, text_in=None):
        self.kms_client = kms_client
        self.text_in = text_in

    def encrypt(self, key_id):
        """
        Encrypts text by using the specified key.

        :param key_id: The ARN or ID of the key to use for encryption.
        :return: The encrypted version of the text.
        """
        text_in = self.text_in
        if text_in is None:
            text_in = input("Enter some text to encrypt: ")
        try:
            cipher_text = self.kms_client.encrypt(
                KeyId=key_id, Plaintext=text_in.encode()
            )["CiphertextBlob"]
        except ClientError as err:
            logger.error(
                "Couldn't encrypt text. Here's why: %s",
                err.response["Error"]["Message"],
            )
        else:
            print(f"Your ciphertext is: {cipher_text}")
            return cipher_text

    def decrypt(self, key_id, cipher_text):
        """
        Decrypts text previously encrypted with a key.

        :param key_id: The ARN or ID of the key used to decrypt the data.
        :param cipher_text: The encrypted text to decrypt.
        """
        answer = input("Ready to decrypt your ciphertext (y/n)? ")
        if answer.lower() == "y":
            try:
                text = self.kms_client.decrypt(
                    KeyId=key_id, CiphertextBlob=cipher_text
                )["Plaintext"]
            except ClientError as err:
                logger.error(
                    "Couldn't decrypt your ciphertext. Here's why: %s",
                    err.response["Error"]["Message"],
                )
            else:
                print(f"Your plaintext is {text.decode()}")
        else:
            print("Skipping decryption demo.")

    def re_encrypt(self, source_key_id, cipher_text):
        """
        Takes ciphertext previously encrypted with one key and reencrypt it by using
        another key.

        :param source_key_id: The ARN or ID of the original key used to encrypt the
                              ciphertext.
        :param cipher_text: The encrypted ciphertext.
        :return: The ciphertext encrypted by the second key.
        """
        destination_key_id = input(
            f"Your ciphertext is currently encrypted with key {source_key_id}. "
            f"Enter another key ID or ARN to reencrypt it: "
        )
        if destination_key_id != "":
            try:
                cipher_text = self.kms_client.re_encrypt(
                    SourceKeyId=source_key_id,
                    DestinationKeyId=destination_key_id,
                    CiphertextBlob=cipher_text,
                )["CiphertextBlob"]
            except ClientError as err:
                logger.error(
                    "Couldn't reencrypt your ciphertext. Here's why: %s",
                    err.response["Error"]["Message"],
                )
            else:
                print(f"Reencrypted your ciphertext as: {cipher_text}")
                return cipher_text
        else:
            print("Skipping reencryption demo.")


def key_encryption(kms_client):
    logging.basicConfig(filename=None, level=logging.INFO, format="%(levelname)s: %(message)s")

    print("-" * 88)
    print("Welcome to the AWS Key Management Service (AWS KMS) key encryption demo.")
    print("-" * 88)

    #key_id = input("Enter a key ID or ARN to start the demo: ")
    key_id = settings.KEY_MAIN_ID
    if key_id == "":
        print("A key is required to run this demo.")
        return

    text_in = "welcome message everything looks ok"

    key_encrypt = KeyEncrypt(kms_client, text_in=text_in)
    cipher_text = key_encrypt.encrypt(key_id)
    print("-" * 88)
    if cipher_text is not None:
        key_encrypt.decrypt(key_id, cipher_text)
        print("-" * 88)
        #key_encrypt.re_encrypt(key_id, cipher_text)

    print("\nThanks for watching!")
    print("-" * 88)


if __name__ == "__main__":
    try:
        #key_encryption(boto3.client("kms"))
        kms_session = boto3.Session(
            aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
            aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
            region_name="us-east-2"
        )
        kms_client = kms_session.client("kms")
        key_encryption(kms_client)

    except Exception:
        logging.exception("Something went wrong with the demo!")


