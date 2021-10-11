import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.config import Config


def kinesis_create_client():
    my_config = Config(
        region_name = 'us-west-2',
        signature_version = 'v4',
        retries = {
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    client = boto3.client('kinesis', config=my_config)
    return client


def dynamodb_create_client1(): # ok
    client = boto3.resource('dynamodb', region_name="us-west-2")
    return client    

def dynamodb_create_client2(): # ok
    my_config = Config(
        region_name = 'us-west-2',
        signature_version = 'v4',
        retries = {
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    client = boto3.resource('dynamodb', config=my_config)
    return client    


def lambda_handler(event, context):
       
    response = "The method not defined"
    client = dynamodb_create_client1()

    table = client.Table("dojotable1")
       
    if (event["method"] == "getTask"):
           
        response = table.get_item(Key={'primarykey': event["arguments"]["id"], 'secondarykey':"ok"})
        return response
           
    elif (event["method"] == "addTask"):
           
        response = table.put_item(Item={'primarykey': event["arguments"]["id"], 'secondarykey':"ok", 'description': event["arguments"]["description"]})
        return response

    elif (event["method"] == "queryAllTask"):
           
        response = table.query( KeyConditionExpression=Key('primarykey').eq(0) )
        return response
           
    else:
        return response


if __name__ == '__main__':
    context_in = {}

    event_in = {"method":"queryAllTask",
                "arguments" :
                    { "id":0 }
                }
    rv = lambda_handler(event_in, context_in)
    print("rv: ", rv)

    #event_in = {"method":"addTask",
    #            "arguments" :
    #                { "id":1, "description":"first task" }
    #            }
    #rv = lambda_handler(event_in, context_in)
    #print("rv: ", rv)

    event_in = {"method":"getTask",
                "arguments" :
                    { "id":0 }
                }
    rv = lambda_handler(event_in, context_in)
    print("rv: ", rv)


