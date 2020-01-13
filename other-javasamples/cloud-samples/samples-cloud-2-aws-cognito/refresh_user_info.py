#!/usr/bin/env python
# refresh_user_info.py

# https://medium.com/@houzier.saurav/private-api-endpoints-with-api-gateway-authorizers-and-cognito-249c288b0ab8

import boto3
import botocore.exceptions
import json

USER_POOL_ID = ''
CLIENT_ID = ''
CLIENT_SECRET = ''


def error_message(msg):
    return {'message': msg, "error": True, "success": False, "data": None}

def lambda_handler(event, context):
    any_field_ok = False
    for field in ["access_token", "username"]:
        if event.get(field) is not None:
            any_field_ok = True
    if not any_field_ok:
        return error_message("Please provide {field} to renew tokens")

    client = boto3.client('cognito-idp')
    try:
        # $$ if you want to get user from users access_token
        access_token = event.get("access_token", None)
        if access_token is not None:
            response = client.get_user(AccessToken=access_token)
        else:
            response = client.admin_get_user(
                UserPoolId=USER_POOL_ID,
                Username=event["username"]
            )

    except client.exceptions.UserNotFoundException as e:
        return error_message("Invalid username ")

    return {
        "error": False,
        "success": True,
        "data": response["UserAttributes"],
        'message': None,
    }

