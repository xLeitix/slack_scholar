from __future__ import print_function

import json
import logging
import sys, os
from urlparse import parse_qs
from boto3 import client as boto3_client

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

    lambda_client.invoke(FunctionName="slack-scholar-backend",
                                           InvocationType='Event',
                                           Payload=json.dumps(
                                            {"function":"showpaper",
                                             "author":author,
                                             "searchstring":searchstring,
                                             "response_url":response_url
                                            }))

    resp_string = "@%s asked me to look for \"%s\" (author) and \"%s\" (searchstring). I'll be right back." % (user, author, searchstring)
    return {'text' : resp_string, 'response_type' : 'in_channel'}
