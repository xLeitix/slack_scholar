from __future__ import print_function

import json
import logging
import sys, os
from urlparse import parse_qs
from boto3 import client as boto3_client

# get this file's directory independent of where it's run from
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./lib"))
sys.path.append(os.path.join(here, "./vendored"))

log = logging.getLogger()
log.setLevel(logging.DEBUG)

lambda_client = boto3_client('lambda')

def handler(event, context):

    req_body = event['body']
    params = parse_qs(req_body)

    command = params['text'][0]
    response_url = params['response_url'][0]
    user = params['user_name'][0]

    author, searchstring = command.split(" ", 1)

    lambda_client.invoke(FunctionName="scholar-slack-backend",
                                           InvocationType='Event',
                                           Payload=json.dumps(
                                            {"author":author,
                                             "searchstring":searchstring,
                                             "response_url":response_url
                                            }))

    return "I'm on it."
