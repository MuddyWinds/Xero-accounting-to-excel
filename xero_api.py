import base64
import json
import webbrowser
import requests
import pandas as pd
from pathlib import Path

from config import CLIENT_ID, CLIENT_SECRET
from reformat import reformatting_json


# Client_id and secret generated from the xero account
# scope: Only read balance sheets at current stage
# To get a refresh token, you must request the offline_access scope.
# A refresh token allows you to refresh your access token and maintain an offline connection.
redirect_url = "https://xero.com"
scope = "offline_access accounting.reports.read"
b64_id_secret = base64.b64encode(bytes(CLIENT_ID + ":" + CLIENT_SECRET, 'utf-8')).decode('utf-8')


def xero_first_auth():
    # Send a request, allow our app to access to our account.
    auth_url = ('''https://login.xero.com/identity/connect/authorize?''' +
                '''response_type=code''' +
                '''&client_id=''' + CLIENT_ID +
                '''&redirect_uri=''' + redirect_url +
                '''&scope=''' + scope +
                '''&state=123''')
    webbrowser.open_new(auth_url)

def xero_auth_url(auth_res_url):
    # Users are redirected back to you with a code
    start_number = auth_res_url.find("code=") + len("code=")
    end_number = auth_res_url.find("&scope")
    auth_code = auth_res_url[start_number:end_number]

    # Exchange the code
    exchange_code_url = "https://identity.xero.com/connect/token"
    response = requests.post(exchange_code_url,
                             headers={'Authorization': 'Basic ' + b64_id_secret},
                             data={'grant_type': "authorization_code",
                                   "code": auth_code,
                                   "redirect_uri": redirect_url})
    json_response = response.json()

    # Receive the tokens
    return [json_response['access_token'], json_response['refresh_token']]
    

# Check the full set of tenants that have been authorized to access
def xero_tenants(access_token):
    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url,
                            headers = {'Authorization': 'Bearer ' + access_token,
                                       'Content-Type': 'application/json'
                                       })
    json_response = response.json()

    for tenants in json_response:
        json_dict = tenants
    return json_dict['tenantId']

# Refresh access tokens
def xero_refresh_token(refresh_token):
    token_refresh_url = 'https://identity.xero.com/connect/token'
    response = requests.post(token_refresh_url,
                             headers = {
                                 'Authorization': 'Basic ' + b64_id_secret,
                                 'Content-Type': 'application/x-www-form-urlencoded'
                             },
                             data = {
                                 'grant_type': 'refresh_token',
                                 'refresh_token': refresh_token
                             })
    json_response = response.json()

    new_refresh_token = json_response['refresh_token']
    rt_file = open(str(Path.home() / "Downloads") + "/refresh_token.txt", 'w')
    rt_file.write(new_refresh_token)
    rt_file.close()

    return [json_response['access_token'], json_response['refresh_token']]


# Call the API
def xero_request():
    old_refresh_token = open(str(Path.home() / "Downloads") + "/refresh_token.txt", 'r').read()
    new_tokens = xero_refresh_token(old_refresh_token)
    xero_tenant_id = xero_tenants(new_tokens[0])

    get_url = 'https://api.xero.com/api.xro/2.0/Reports/BalanceSheet'
    response = requests.get(get_url,
                            headers = {
                                'Authorization': 'Bearer ' + new_tokens[0],
                                'Xero-tenant-id': xero_tenant_id,
                                'Accept': 'application/json'
                            })
    json_response = response.json()
    reformatting_json(json_response["Reports"][0]["Rows"], json_response["Reports"][0]["ReportTitles"])
