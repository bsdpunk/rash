import sys
import requests
import json
from pprint import pprint


#def set_cloud_network(imp_token, region, net_label):
#
#
#    #add fucking x-auth-token
#    headers = {'content-type': 'application/json', "X-Auth-Token":imp_token}
#    payload = {'network': {'name': net_label}}
#    #payload =  json.loads(payload)
#    #print(payload)
#    r = requests.post("https://"+region+".networks.api.rackspacecloud.com/v2.0/networks", data=json.dumps(payload), headers=headers)
#    #print(r.text)
#    json_data = json.loads(r.text)
#
#    return(json_data)



def get_images(imp_token, ddi, region):
    headers = {'content-type': 'application/json', "X-Auth-Token":imp_token}
    endpoint = "https://"+ region +".images.api.rackspacecloud.com/v2/"+ddi+"/images"
    #"https://"+ region +".networks.api.rackspacecloud.com/v2.0/networks"
    #print(endpoint)
    #print(headers)
    r = requests.get(endpoint, headers=headers)
    #print(r.text)
    json_data = json.loads(r.text) 

    return(json_data)

#def create_image(imp_token, ddi, region, flavor, name):
#    headers = {'content-type': 'application/json', "X-Auth-Token":imp_token}
#    endpoint = "https://"+ region +".servers.api.rackspacecloud.com/v2/"+ddi+"/servers"
#    #"https://"+ region +".networks.api.rackspacecloud.com/v2.0/networks"
#    #print(endpoint)
#    #print(headers)
#    r = requests.get(endpoint, headers=headers)
#    #print(r.text)
#    json_data = json.loads(r.text) 
#
#    return(json_data)
