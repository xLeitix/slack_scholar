# Scholar-Slack

## A set of AWS Lambda Based Slack Commands for Google Scholar

This simple Python bot brings two new commands to your [Slack](https://slack.com) team:

`/bibtex [author lastname] [searchstring]`

(finds a Bibtex entry for a given paper)

<img src="https://github.com/xLeitix/slack_scholar/raw/master/img/bibtex_cmd.png" alt="Example /bibtex command" style="width: 200px;"/>

`/whois [author searchstring]`

(displays Google Scholar author information about a researcher)

<img src="https://github.com/xLeitix/slack_scholar/raw/master/img/whois_cmd.png" alt="Example /whois command" style="width: 200px;"/>

That's it. That's pretty much all the bot does for now :)

### Caveat Emptor

Google Scholar rate-limits its API pretty aggressively.
This means two things:

1. If you send many requests within short time (where *many* may mean as little as 10 or 20 within a few minutes), Google will stop responding.
2. Even if you *don't* send many requests, sometimes Google will not respond anyway, simply because somebody else with the same IP address has sent too many requests (the bot is running in AWS, after all).

The error we receive is hard to distinguish from a failed search, so what you will see is the following:

<img src="https://github.com/xLeitix/slack_scholar/raw/master/img/failed_to_find.png" alt="API Limit Error" style="width: 500px;"/>

This can mean *either* that we are currently over the rate limit, or that your search just did not find anything. In the former case, you will need to wait (at least an hour or two, in most cases). In the latter case, you can try again with a different search string.

__If you know how to handle the Google API limit better, contact me, or even better, send a pull request!__
