#!/usr/bin/env python
# refresh_user_info_verify.py

# https://medium.com/@houzier.saurav/private-api-endpoints-with-api-gateway-authorizers-and-cognito-249c288b0ab8

import boto3
import botocore.exceptions
import json

USER_POOL_ID = ''
CLIENT_ID = ''
CLIENT_SECRET = ''


reqRec = []

def error_message(msg):
    return {'message': msg, "error": True, "success": False, "data": None}


def lambda_handler(event, context):
    reqRec.append({'event': event})

    '''Output from an Amazon API Gateway Lambda Authorizer 
       https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html
       {    "type":"TOKEN",
            "authorizationToken":"{caller-supplied-token}",
            "methodArn":"arn:aws:execute-api:{regionId}:{accountId}:{apiId}/{stage}/{httpVerb}/[{resource}/[{child-resources}]]"
    }'''
    etype = event.get('type', None)
    eheader = event.get('headers', None)
    etoken = None
    if eheader is not None:
        etoken = eheader.get('user_access_token', None)
    if etype == "REQUEST" and etoken is not None:
        return {
            "principalId": "user",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow",
                        "Resource": "*"
                    }
                ]
            }
        }

    #return {'reqrec': json.dumps(reqRec)}

    any_field_ok = False
    for field in ["user_access_token"]:
        if event.get(field) is not None:
            any_field_ok = True
    if not any_field_ok:
        return error_message("Please provide {field} to verify tokens")

    client = boto3.client('cognito-idp')
    try:
        # $$ if you want to get user from users access_token
        user_access_token = event.get("user_access_token", None)
        response = client.get_user(AccessToken=user_access_token)

    except client.exceptions.UserNotFoundException as e:
        return error_message("Invalid username ")
    except client.exceptions.NotAuthorizedException as e:
        return error_message("Not authorized")
    except:
        return error_message("Unknown exception")

    return {
        "error": False,
        "success": True,
        "data": response["UserAttributes"],
        'message': None,
    }

