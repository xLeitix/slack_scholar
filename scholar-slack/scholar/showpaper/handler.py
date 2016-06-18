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

    command = params['text'][0] if 'text' in params else ""
    response_url = params['response_url'][0]
    user = params['user_name'][0]

    params_splitted = command.split(" ", 1)

    if command == "help" or command == "usage" or len(params_splitted) == 1:
        return {"text":"Usage: /bibtex <author> <searchstring>",
                "attachments" : [
                    {"text":"Example: /bibtex leitner patterns in the chaos"},
                    {"text":"Note that <author> is always just the first word of your argument"}
                ]}

    author, searchstring = params_splitted

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
