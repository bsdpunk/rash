import sys
import requests
import json
from pprint import pprint


def set_cloud_network(imp_token, region, net_label):


    #add fucking x-auth-token
    headers = {'content-type': 'application/json', "X-Auth-Token":imp_token}
    payload = {'network': {'name': net_label}}
    #payload =  json.loads(payload)
    print(payload)
    r = requests.post("https://"+region+".networks.api.rackspacecloud.com/v2.0/networks", data=json.dumps(payload), headers=headers)
    print(r.text)
    json_data = json.loads(r.text)

    return(json_data)



def get_cloud_networks(imp_token, region, ddi):
    headers = {'content-type': 'application/json', "X-Auth-Token":imp_token}
    r = requests.post("https://{region}.servers.api.rackspacecloud.com/v2/{ddi}/os-networksv2")
    fixed = "0"
    return(fixed)
