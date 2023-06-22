import base64
import json
import webbrowser
import requests
import pandas as pd
from pathlib import Path

from config import CLIENT_ID, CLIENT_SECRET
from reformat import reformatting_json

# Constants
REDIRECT_URL = "https://xero.com"
SCOPE = "offline_access accounting.reports.read"

# Encode client_id and client_secret for use in the authorization header
b64_id_secret = base64.b64encode(bytes(CLIENT_ID + ":" + CLIENT_SECRET, 'utf-8')).decode('utf-8')

def xero_first_auth():
    # Construct the auth_url and open it in the browser for user authorization
    auth_url = (f"https://login.xero.com/identity/connect/authorize?response_type=code&client_id={CLIENT_ID}"
                f"&redirect_uri={REDIRECT_URL}&scope={SCOPE}&state=123")
    webbrowser.open_new(auth_url)

def xero_auth_url(auth_res_url):
    # Extract the authorization code from the response URL
    start_number = auth_res_url.find("code=") + len("code=")
    end_number = auth_res_url.find("&scope")
    auth_code = auth_res_url[start_number:end_number]

    # Exchange the authorization code for access and refresh tokens
    exchange_code_url = "https://identity.xero.com/connect/token"
    response = requests.post(exchange_code_url,
                             headers={'Authorization': 'Basic ' + b64_id_secret},
                             data={'grant_type': "authorization_code",
                                   "code": auth_code,
                                   "redirect_uri": REDIRECT_URL})
    json_response = response.json()

    # Return the access and refresh tokens
    return [json_response['access_token'], json_response['refresh_token']]

def xero_tenants(access_token):
    # Get the list of authorized tenants
    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url,
                            headers={'Authorization': 'Bearer ' + access_token,
                                     'Content-Type': 'application/json'
                                     })
    json_response = response.json()

    # Extract and return the tenantId from the JSON response
    for tenant in json_response:
        tenant_id = tenant['tenantId']
    return tenant_id

def xero_refresh_token(refresh_token):
    # Refresh the access token using the refresh token
    token_refresh_url = 'https://identity.xero.com/connect/token'
    response = requests.post(token_refresh_url,
                             headers={'Authorization': 'Basic ' + b64_id_secret,
                                      'Content-Type': 'application/x-www-form-urlencoded'},
                             data={'grant_type': 'refresh_token',
                                   'refresh_token': refresh_token})
    json_response = response.json()

    # Save the new refresh token to a file
    new_refresh_token = json_response['refresh_token']
    rt_file_path = str(Path.home() / "Downloads") + "/refresh_token.txt"
    with open(rt_file_path, 'w') as rt_file:
        rt_file.write(new_refresh_token)

    # Return the new access and refresh tokens
    return [json_response['access_token'], json_response['refresh_token']]

def xero_request():
    # Read the old refresh token from the file and refresh the tokens
    rt_file_path = str(Path.home() / "Downloads") + "/refresh_token.txt"
    old_refresh_token = open(rt_file_path, 'r').read()
    new_tokens = xero_refresh_token(old_refresh_token)

    # Get the tenant ID
    xero_tenant_id = xero_tenants(new_tokens[0])

    # Call the Xero API to get the balance sheet report
    get_url = 'https://api.xero.com/api.xro/2.0/Reports/BalanceSheet'
    response = requests.get(get_url,
                            headers={'Authorization': 'Bearer ' + new_tokens[0],
                                     'Xero-tenant-id': xero_tenant_id,
                                     'Accept': 'application/json'})
    json_response = response.json()

    # Reformat the JSON response and save it to an Excel file
    reformatting_json(json_response["Reports"][0]["Rows"], json_response["Reports"][0]["ReportTitles"])
