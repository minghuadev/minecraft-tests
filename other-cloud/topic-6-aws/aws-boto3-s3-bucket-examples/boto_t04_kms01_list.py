#
# docs.aws.amazon.com/code-library/latest/ug/python_3_kms_code_examples.html

import boto3
from botocore.exceptions import ClientError
import settings
from pprint import pprint, pformat
import logging

logger = logging.getLogger(__name__)


class KeyManager:
    def __init__(self, kms_client):
        self.kms_client = kms_client
        self.created_keys = []

    def list_keys(self):
        """
        Lists the keys for the current account by using a paginator.
        """
        try:
            page_size = 10
            print("\nLet's list your keys.")

            sel_keys_or_aliases = True
            if sel_keys_or_aliases:
                # need ListKeys permission on all resources
                key_paginator = self.kms_client.get_paginator("list_keys")
                kk = "Keys"
            else:
                # need ListAliases permission on all resources
                key_paginator = self.kms_client.get_paginator("list_aliases")
                kk = "Aliases"

            for key_page in key_paginator.paginate(PaginationConfig={"PageSize": 10}):
                print(f"Here are {len(key_page[kk])} keys:")
                if type(key_page[kk]) is list:
                    print("[")
                    for k in key_page[kk]:
                        tgt = None
                        if type(k) is dict:
                            tgt = k.get("TargetKeyId", None)
                        if tgt is not None or sel_keys_or_aliases:
                            out_strs = pformat(k, indent=2).splitlines()
                            for out_line in out_strs:
                                print("  ", out_line)
                        else:
                            print("      ... skip ... ", 
                                  str(k.get("AliasName", "unknown")) )
                    print("]")
                else:
                    pprint(key_page[kk])
                if key_page["Truncated"]:
                    answer = input(
                        f"Do you want to see the next {page_size} keys (y/n)? "
                    )
                    if answer.lower() != "y":
                        break
                else:
                    print("That's all your keys!")
        except ClientError as err:
            logging.error(
                "Couldn't list your keys. Here's why: %s",
                err.response["Error"]["Message"],
            )
        except Exception as err:
            logging.error(
                "Couldn't list your keys. Here's why: %s",
                "Exception: ", str(err),
            )


if __name__ == "__main__":
    try:
        #key_encryption(boto3.client("kms"))
        kms_session = boto3.Session(
            aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
            aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
            region_name="us-east-2"
        )
        kms_client = kms_session.client("kms")
        kms_mgr = KeyManager(kms_client)
        kms_mgr.list_keys()

    except Exception:
        logging.exception("Something went wrong with the demo!")


