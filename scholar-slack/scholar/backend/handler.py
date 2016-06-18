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
import scholarly

def handler(event, context):

    log.info(str(event))

    if event['function'] == 'showpaper':
        resp = query_scholar_for_papers(event['author'], event['searchstring'])
    elif event['function'] == 'showauthor':
        resp = query_scholar_for_author_profile(event['author'])
    else:
        resp = "Invalid function."

    requests.post(event['response_url'], json={"text" : resp, "response_type" : "in_channel"})
    return

def query_scholar_for_papers(author, searchstring):

    querier = ScholarQuerier()
    settings = ScholarSettings()
    settings.set_citation_format(settings.CITFORM_BIBTEX)
    settings.set_per_page_results(5)
    querier.apply_settings(settings)
    query = SearchScholarQuery()
    query.set_author(author)
    query.set_phrase(searchstring)

    querier.send_query(query)

    return_str = ''
    if len(querier.articles) > 0:
        return_str += querier.articles[0].as_citation() + '\n'
    else:
        return_str = 'Ooopsie. No results. Maybe we ran over the request limit?'

    return return_str

def query_scholar_for_author_profile(author):

    try:
        _author = next(scholarly.search_author(author))
    except:
        return "Ooopsie. Maybe we ran over the request limit?"

    if _author == None:
        return "Did not find a profile for %s" % author

    resp_str = ""
    resp_str += (_author.name + "\n")
    resp_str += (_author.affiliation + "\n")
    for interest in _author.interests:
        resp_str += (interest + ' - ')
    resp_str += "\n"
    resp_str += ("https://scholar.google.ch/citations?user=" + _author.id)

    return resp_str
