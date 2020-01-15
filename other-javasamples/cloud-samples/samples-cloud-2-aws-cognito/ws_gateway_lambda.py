#!/usr/bin/env python
# ws_gateway_lambda.py

import json

eventRecord = []
eventCount = 0
connCount = 0


def lambda_handler(event, context):
    global eventCount
    eventCount += 1

    is_conn = event.get('requestContext', None)
    if is_conn is not None:
        conn_id = is_conn.get('connectionId', None)
        conn_route = is_conn.get('routeKey', None)
        if conn_route is not None and conn_route == '$connect' and conn_id is not None:
            global connCount
            connCount += 1
            eventRecord.append({'conn_id': conn_id, 'conn_evtcnt': eventCount, 'conn_count': connCount})
    else:
        conn_id = None

    ret_data = {'received': str(event),
                'returning': 'hellow client. eventCount %d connCount %d' % (eventCount, connCount),
                'conn_id': conn_id,
                'records': str(eventRecord)}

    return {
        'statusCode': 200,
        'body': json.dumps(ret_data)
    }

