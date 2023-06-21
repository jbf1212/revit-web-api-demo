import posixpath
import json
import requests

from System.Net import WebClient

BASE_ID = "app7GoC6paABCDEFG" # This is a fake base id. Replace this with your own base id once you have it
AIRTABLE_API_KEY = "key7cmK9j2ABCDEFG" # This is a fake key, you need to get your own from airtable
TABLE_NAME = "Materials"

VERSION = "v0"
API_BASE_URL = "https://api.airtable.com/"

url = posixpath.join(API_BASE_URL, VERSION, BASE_ID, TABLE_NAME)

########################################################
# GET REQUESTS (two functions below do the same thing)
########################################################

def get_request_webclient(request_url):
    '''
    Make a get request using WebClient
    '''
    client = WebClient()
    client.Headers.Add("Authorization", "Bearer {}".format(AIRTABLE_API_KEY))

    response = client.DownloadString(request_url)
    json_response = json.loads(response)
    return json_response

def get_request_requests(request_url):
    '''
    Make a get request using Python requests module
    '''
    headers = {"Authorization": "Bearer {}".format(AIRTABLE_API_KEY)}
    response = requests.get(request_url, headers=headers)
    json_response = response.json()

    return json_response


########################################################
# PATCH REQUESTS (two functions below do the same thing)
########################################################

def patch_request_webclient(request_url, data):
    '''
    Make a patch request using WebClient
    '''
    client = WebClient()
    client.Headers.Add("Authorization", "Bearer {}".format(AIRTABLE_API_KEY))
    client.Headers.Add("Content-Type", "application/json")

    response = client.UploadString(request_url, "PATCH", json.dumps(data))
    return response

def patch_request_requests(request_url, data):
    '''
    Make a patch request using requests module
    '''
    json_data = json.dumps(data)
    headers = {"Authorization": "Bearer {}".format(AIRTABLE_API_KEY), "Content-Type":"application/json"}

    response = requests.patch(request_url, data=json_data, headers=headers)
    return response