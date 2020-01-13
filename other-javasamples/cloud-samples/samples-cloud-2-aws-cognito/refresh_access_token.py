#!/usr/bin/env python
# refresh_access_token.py

# https://medium.com/@houzier.saurav/private-api-endpoints-with-api-gateway-authorizers-and-cognito-249c288b0ab8

import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json

USER_POOL_ID = ''
CLIENT_ID = ''
CLIENT_SECRET =''


def error_message(msg):
    return {'message': msg, "error": True, "success": False, "data": None}

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def lambda_handler(event, context):
    for field in ["username", "refresh_token"]:
        if event.get(field) is None:
            return error_message("Please provide {field} to renew tokens")
    client = boto3.client('cognito-idp')
    username = event["username"]
    refresh_token = event["refresh_token"]

    secret_hash = get_secret_hash(username)
    try:
        resp = client.initiate_auth(
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': secret_hash,
                'REFRESH_TOKEN': refresh_token,
            },
            ClientId=CLIENT_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
        )
        res = resp.get("AuthenticationResult")
    except client.exceptions.NotAuthorizedException as e:
        return error_message("Invalid refresh token or username is incorrect or Refresh Token has been revoked")
    except client.exceptions.UserNotConfirmedException as e:
        return error_message("User is not confirmed")
    except Exception as e:
        return error_message(e.__str__())

    if res:
        return {'message': "success",
                "error": False,
                "success": True,
                "data": {
                    "id_token": res["IdToken"],
                    "access_token": res["AccessToken"],
                    "expires_in": res["ExpiresIn"],
                    "token_type": res["TokenType"]       }}

    return

