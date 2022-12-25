import boto3
import time
from pprint import pprint as pp


def create_movie_table(dynamodb=None):
    if not dynamodb:
        #dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
        dynamodb = boto3.resource('dynamodb', region_name="us-west-2", endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


def describe_movie_table(dynamodb=None):
    #client = boto3.client('dynamodb', region_name="us-west-2")
    client = boto3.client('dynamodb', region_name="us-west-2", endpoint_url="http://localhost:8000")
    response = client.describe_table(TableName='Movies')
    return response



if __name__ == '__main__':
    try:
        movie_table = create_movie_table()
        print("Table status:", movie_table.table_status)
    except:
        print("Exception when creating")
        pass
    
    t0 = time.time()
    ts_last = ""
    while True:
        tnow = time.time()
        tdiff = tnow - t0
        if tdiff > 15 :
            break # 5.5 sec on aws, or 0 local
        resp = describe_movie_table()
        #print("")
        #print("Table response: ", "    at %.3f" % tdiff)
        #pp(resp, indent=4)
        ts = resp.get('Table', {}).get('TableStatus', "Unknown")
        if ts != ts_last:
            print("Table status: ", "%12s" % ts, "  at %.3f" % tdiff )
            ts_last = ts
        if type(ts) is str and ts == 'ACTIVE':
            break
        time.sleep(0.01)
    

    
