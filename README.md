# Scholar-Slack

## A set of AWS Lambda Based Slack Commands for Google Scholar

This simple Python bot brings two new commands to your [Slack](https://slack.com) team:

`/bibtex [author lastname] [searchstring]`

(finds a Bibtex entry for a given paper)

<img src="https://github.com/xLeitix/slack_scholar/raw/master/img/bibtex_cmd.png" alt="Example /bibtex command" style="width: 500px;"/>

`/whois [author searchstring]`

(displays Google Scholar author information about a researcher)

<img src="https://github.com/xLeitix/slack_scholar/raw/master/img/whois_cmd.png" alt="Example /whois command" style="width: 500px;"/>

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

## Installation

Installing this Slack integration has two parts: creating a new instance of the bot in AWS, and configuring the integration for your team. __Currently, each instance of the bot only supports one team at a time. [Log a bug](https://github.com/xLeitix/slack_scholar/issues) if you require multi-team support.__

### Prerequisites

Scholar-Slack runs in [AWS Lambda](http://docs.aws.amazon.com/lambda/latest/dg/welcome.html). For deployment to Lambda, the project uses the [Serverless framework](http://www.serverless.com). Hence, you will need the following to start using Scholar-Slack:

* A Slack team where you are allowed to install integrations. Duh.
* An [AWS account](https://aws.amazon.com). I *think* a free tier account is *not* sufficient, as I don't think that the free tier covers Lambda, but you should check yourself. In any way, the actual costs to you for using Scholar-Slack in AWS should be negligible, as Lambda is very cheap and we are not really using much else from AWS.
* A local installation of the [Serverless framework](http://www.serverless.com). Follow the installation instructions on the web page. This will be used in the following to deploy to Amazon.

### Installation Instructions

__Step 1 - Configuring Slack, Part 1__

* In your Slack client, select __Apps & Integrations__. This opens up the Web interface. Select __Manage__ on the upper-right corner. Select __Custom Integrations__ on the left-hand pane.

* Select __Slash Commands__, and then __Add Configuration__.

* Type `/bibtex` as a new command in the field, and select __Add Slash Command Integration__.

* In the following form, save the _Token_ somewhere. We will need this later. Enter some dummy value into the __URL__ field, such as *http://dummy.com*. Give the integration a useful name, and upload a nice icon (I am using a Google Scholar icon). Click __Save Integration__.

* Repeat the same two steps for a second command, `/whois`. Again save the token (and remember which token is which).

__Step 2 - Installing the Bot__

* Clone the source code:

`git clone https://github.com/xLeitix/slack_scholar.git`

* Save the tokens of your project. Go to the *scholar-slack* directory and run:

`echo "TOKEN" > scholar/showpaper/lib/token.secret`

(replacing *TOKEN* for the token that you copied from the */bibtex* command), and

`echo "TOKEN" > scholar/showauthor/lib/token.secret`

(with the token that you saved from the */whois* command)

* Create a new Serverless project.

`serverless project create --region us-east-1 --name scholar-slack --domain DOMAIN`

(obviously replace DOMAIN for some unique domain - you don't need to *own* this domain, and it really does not matter much except that it is unique)

Answer the questions Serverless asks you. You may need to create an AWS profile with your account data if you don't have one. The stage name is not relevant - the default *dev* is fine. This step will take a while, as Serverless will use CloudFormation to create a bunch of resources.

* Deploy the project using Serverless' interactive Dash utility. Run:

`serverless dash deploy`

Select all functions and endpoints, and then run __Deploy__  (just hitting the space bar 6 times should do the trick). When Dash is done, it will output two endpoint addresses. We need those to finish configuring Slack.

__Step 3 - Configuring Slack, Part 2__

* Go back to the __Apps & Integrations__ pane, and edit your two new Slash commands. Replace the __URL__ for the */bibtex* command with the endpoint ending in */showpaper*, and the __URL__ for */whois* with the endpoint ending in */showauthor* (remember, the endpoints come from the output from the Dash utility). Save your integrations.

* If everything is well, your commands are now functional. Go to your Slack client, and test them (for instance in the *slackbot* window). Don't worry if the commands time out the first time - bootstrapping Lambda seems to take a while, and Slack requires an answer within 3 seconds.
