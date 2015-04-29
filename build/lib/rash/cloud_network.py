import sys
import requests
import json
from pprint import pprint


def set_cloud_network(imp_token, region, net_label):


    #add fucking x-auth-token
    headers = {'content-type': 'application/json', "X-Auth-Token":imp_token}
    payload = {'network': {'name': net_label}}
    #payload =  json.loads(payload)
    #print(payload)
    r = requests.post("https://"+region+".networks.api.rackspacecloud.com/v2.0/networks", data=json.dumps(payload), headers=headers)
    #print(r.text)
    json_data = json.loads(r.text)

    return(json_data)

def create_cloud_subnet(imp_token, region, net_label, cidr):

    cloud_networks = get_cloud_networks(imp_token, region)
    #cloud_networks = json.loads(cloud_networks)
    for item in cloud_networks["networks"]:
        if item['name'] == net_label:
            print(item['id'])
            net_uuid = item['id']
    
    if 'net_uuid' in locals():
        print("Adding to existing Neutron network")
    else:
        new_network = set_cloud_network(imp_token, region, net_label)
        net_uuid = new_network['network']['id']

    #need to get uuid from label
    #add fucking x-auth-token
    headers = {'content-type': 'application/json', "X-Auth-Token":imp_token}
    payload = {"subnet": { "network_id":net_uuid,"ip_version": "4", "cidr":cidr}}
    #payload =  json.loads(payload)
    #print(payload)
    r = requests.post("https://"+region+".networks.api.rackspacecloud.com/v2.0/subnets", data=json.dumps(payload), headers=headers)
    #print(r.text)
    json_data = json.loads(r.text)

    return(json_data)





def get_cloud_networks(imp_token, region):
    headers = {'content-type': 'application/json', "X-Auth-Token":imp_token}
    endpoint = "https://"+ region +".networks.api.rackspacecloud.com/v2.0/networks"
    #print(endpoint)
    #print(headers)
    r = requests.get(endpoint, headers=headers)
    #print(r.text)
    json_data = json.loads(r.text) 

    return(json_data)
