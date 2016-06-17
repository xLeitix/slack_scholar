from __future__ import print_function

import json
import logging
import sys, os

log = logging.getLogger()
log.setLevel(logging.DEBUG)

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./lib"))
sys.path.append(os.path.join(here, "./vendored"))

import requests
from scholar import ScholarQuerier, ScholarSettings, SearchScholarQuery

def handler(event, context):

    log.info(str(event))

    querier = ScholarQuerier()
    settings = ScholarSettings()
    settings.set_citation_format(settings.CITFORM_BIBTEX)
    settings.set_per_page_results(5)
    querier.apply_settings(settings)
    query = SearchScholarQuery()
    query.set_author(event['author'])
    query.set_phrase(event['searchstring'])

    log.info("Ready to query GS")

    querier.send_query(query)

    log.info("Received answer from GS")

    return_str = ''
    for article in querier.articles:
        return_str += article.as_citation() + '\n'
    if return_str == '':
        return_str = 'Ooopsie. No results. Maybe we ran over the request limit?'

    log.info("Returning back to Slack")
    log.info("All done")

    requests.post(event['response_url'], json={"text" : return_str, "response_type" : "in_channel"})
    return
