#!/usr/bin/env python
import requests
import sys, os, urllib, json, webbrowser
from boto.sts import STSConnection


if len(sys.argv) == 3:
    account_id_from_user = sys.argv[1]
    role_name_from_user = sys.argv[2]
else:
    print "\n\tUsage: ",
    print os.path.basename(sys.argv[0]), # script name
    print " <account_id> <role_name>"
    exit(0)


role_arn = "arn:aws:iam::" + account_id_from_user + ":role/"
role_arn += role_name_from_user


sts_connection = STSConnection()
assumed_role_object = sts_connection.assume_role(
    role_arn=role_arn,
    role_session_name="AssumeRoleSession"
)


access_key = assumed_role_object.credentials.access_key
session_key = assumed_role_object.credentials.secret_key
session_token = assumed_role_object.credentials.session_token
json_temp_credentials = '{'
json_temp_credentials += '"sessionId":"' + access_key + '",'
json_temp_credentials += '"sessionKey":"' + session_key + '",'
json_temp_credentials += '"sessionToken":"' + session_token + '"'
json_temp_credentials += '}'


request_parameters = "?Action=getSigninToken"
request_parameters += "&Session="
request_parameters += urllib.quote_plus(json_temp_credentials)
request_url = "https://signin.aws.amazon.com/federation"
request_url += request_parameters
r = requests.get(request_url)


sign_in_token = json.loads(r.text)["SigninToken"]


request_parameters = "?Action=login"
request_parameters += "&Issuer="
request_parameters += "&Destination="
request_parameters += urllib.quote_plus("https://console.aws.amazon.com/")
request_parameters += "&SigninToken=" + sign_in_token
request_url = "https://signin.aws.amazon.com/federation"
request_url += request_parameters


webbrowser.open(request_url)
