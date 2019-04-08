import boto3
import json
import logging
import os

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# The base-64 encoded, encrypted key (CiphertextBlob) stored in the kmsEncryptedHookUrl environment variable
ENCRYPTED_HOOK_URL = os.environ['kmsEncryptedHookUrl']
# The Slack channel to send a message to stored in the slackChannel environment variable
SLACK_CHANNEL = os.environ['slackChannel']

HOOK_URL = "https://" + boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_HOOK_URL))['Plaintext'].decode('utf-8')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def notify(event, context):
    logger.info("SLACK_CHANNEL: " + str(SLACK_CHANNEL))
    logger.info("HOOK_URL: " + str(HOOK_URL))
    
    logger.info("Event: " + str(event))

    project = event["detail"]["project-name"]
    state = event["detail"]["build-status"]
    
    logger.info("project: " + str(project))
    logger.info("state: " + str(state))
    
    slack_message = {
        'channel': SLACK_CHANNEL,
        'text': "CodeBuild: %s - %s" % (project, state)
    }
    
    req = Request(HOOK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
