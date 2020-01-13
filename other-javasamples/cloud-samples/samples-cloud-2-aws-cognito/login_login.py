#!/usr/bin/env python
# login_login.py

# https://medium.com/@houzier.saurav/aws-cognito-with-python-6a2867dd02c6

import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json

USER_POOL_ID = ''
CLIENT_ID = ''
CLIENT_SECRET = ''


def get_secret_hash(username):
  msg = username + CLIENT_ID
  dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
  msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
  d2 = base64.b64encode(dig).decode()
  return d2

def initiate_auth(client, username, password):
    secret_hash = get_secret_hash(username)
    try:
        resp = client.admin_initiate_auth(
                 UserPoolId=USER_POOL_ID,
                 ClientId=CLIENT_ID,
                 AuthFlow='ADMIN_NO_SRP_AUTH',
                 AuthParameters={
                     'USERNAME': username,
                     'SECRET_HASH': secret_hash,
                     'PASSWORD': password,
                     },
                 ClientMetadata={
                     'username': username,
                     'password': password,              })
    except client.exceptions.NotAuthorizedException:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException:
        return None, "User is not confirmed"
    except Exception as e:
        return None, e.__str__()
    return resp, None

def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    for field in ["username", "password"]:
     if event.get(field) is None:
       return  {"error": True,
                "success": False,
                "message": "{field} is required",
                "data": None}
    resp, msg = initiate_auth(client, event.get("username"), event.get("password"))
    if msg != None:
      return {'message': msg,
              "error": True, "success": False, "data": None}
    if resp.get("AuthenticationResult"):
      return {'message': "success",
               "error": False,
               "success": True,
               "data": {
                   "id_token": resp["AuthenticationResult"]["IdToken"],
                  "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                  "access_token": resp["AuthenticationResult"]["AccessToken"],
                  "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                  "token_type": resp["AuthenticationResult"]["TokenType"]
            }}
    else: #this code block is relevant only when MFA is enabled
        return {"error": True,
           "success": False,
           "data": None, "message": None}

