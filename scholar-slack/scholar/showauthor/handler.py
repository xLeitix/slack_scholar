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

    author = params['text'][0] if 'text' in params else ""
    response_url = params['response_url'][0]
    user = params['user_name'][0]

    if author == "help" or author == "usage" or author == "":
        return {"text":"Usage: /whois <authorname>",
                "attachments" : [
                    {"text":"Example: /whois philipp leitner"}
                ]}

    lambda_client.invoke(FunctionName="slack-scholar-backend",
                                           InvocationType='Event',
                                           Payload=json.dumps(
                                            {"function":"showauthor",
                                             "author":author,
                                             "response_url":response_url
                                            }))

    resp_string = "@%s asked me to look for a Google Scholar profile for \"%s\". I'll get cracking immediately." % (user, author)
    return {'text' : resp_string, 'response_type' : 'in_channel'}
