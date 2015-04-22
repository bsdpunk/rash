import sys
import requests
import json
from pprint import pprint


def set_cloud_network(token, region, ddi, net_range, net_label):


#add fucking x-auth-token
    headers = {'content-type': 'application/json', "X-Auth-Token":token}
    payload = {"network": {"cidr": net_range, "label": net_label}}

    r = requests.post("https://"+region+".servers.api.rackspacecloud.com/v2/"+ddi+"/os-networksv2", data=json.dumps(payload), headers=headers)

    json_data = json.loads(r.text)

    return(json_data)


#json_tickets = get_high_ticket(sys.argv[1])


#for tickets in json_tickets['queue_preview']['tickets']:   
    #print tickets
    #tickets_json = json.loads(tickets)
#    print(tickets['priority'])
#    print(tickets['group_id'])
#    print(tickets['team'])
#    print(tickets['links'])
#    for groups in json_tickets['queue_preview']['tickets'][0]:
#        print groups
#priority
#team
#group_id
#links


def get_cloud_networks(token, region, ddi):
    fixed = "0"
    return(fixed)
