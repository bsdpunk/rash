from __future__ import print_function
import xml.etree.ElementTree as ET
import re
import readline
import threading
import sys
import requests
import json
import os
from pprint import pprint

arg_count = 0
no_auth = 0
server_count = 0

for arg in sys.argv:
    arg_count += 1
#import warnings
#warnings.filterwarnings("ignore")

config_file = os.path.expanduser('~/.rash')

if os.path.isfile(config_file):
    config=open(config_file, 'r')
    config=json.load(config)
else:
    username = raw_input("Username:")
    password = raw_input("Password:")
    config= {"default":[{"username":username,"password":password}]} 
#config=open('.apyi')

def get_racker_token(config):
    username = config["default"][0]["username"]
    password = config["default"][0]["password"]

    headers = {'content-type': 'application/json'}
    payload = {"auth":{"RAX-AUTH:domain":{"name":"Rackspace"},"passwordCredentials":{"username":username,"password":password}}}
    r = requests.post("https://identity-internal.api.rackspacecloud.com/v2.0/tokens", data=json.dumps(payload), headers=headers)
    json_data = json.loads(r.text)

    racker_token = json_data["access"]["token"]["id"]
    return(racker_token)
#print("Token: " + racker_token)
PROMPT = '> '


if arg_count == 2:
    command = sys.argv[1]
    if command == "noauth":
        no_auth = 1

if no_auth == 1:
    racker_token =0
else:
    racker_token = get_racker_token(config)

tokens = {}
servers = {}
#def interrupt():
#    print() # Don't want to end up on the same line the user is typing on.
#    print('Interrupts are not currently accounted for')
#    print(PROMPT, readline.get_line_buffer(), sep='', end='')

def cli():
    while True:
        valid = 0
        cli = str(raw_input(PROMPT))
        if len(cli.split(' ')) ==2:
            command,arguement = cli.split()
            if command == "grackid":
                print(grackid(arguement, racker_token))
                valid = 1
            if command == "gimpuser":
                new_token = gimpuser(arguement, racker_token)
                temp_dict = {arguement:new_token}
                global tokens
                tokens.update(temp_dict)
                valid = 1
            if command == "gservers":
                print(gservers(arguement, racker_token))
                valid = 1
            if command == "gcomplete":
                print(gcomplete(arguement, racker_token))
                global servers
                valid = 1 
            if command == "gusers":
                print(gusers(arguement, racker_token))
                valid = 1
            if command == "imp":
                imp_prompt(arguement, tokens[arguement])
                valid = 1
            if command == "ssh":
                print(ssh_expect(arguement, racker_token))
                valid = 1
			
        if cli == "servers":
            pprint(servers)
            valid = 1
        if cli == "tokens":
            pprint(tokens)
            valid = 1
        if cli == "quit":
            bye()
        if cli == "help":
            print(help_menu())
            valid = 1
        if cli == "mytoken":
            print(racker_token)
            valid = 1


        if valid == 0:
            print("Unrecoginized Command")

def grackid(uuid,token):
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    second_r = requests.get("https://passwords.servermill.rackspace.net/v1/"+uuid+"/password/current", headers=headers)
    return(second_r.text)

def gusers(tenant_id,token):
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    second_r = requests.get("https://customer-admin.prod.dfw1.us.ci.rackspace.net/v3/customer_accounts/CLOUD/"+tenant_id+"/contacts?role=PRIMARY", headers=headers, verify=False)
    root = ET.fromstring(second_r.text)#ET.parse(second_r)
    for child in root.findall('{http://customer.api.rackspace.com/v1}contact'):
        usersname = child.get('username')
        return usersname

#def ssh_line(tenant_id,token):
#    headers = {'content-type': 'application/json',"X-Auth-Token":token}
#    second_r = requests.get("https://customer-admin.prod.dfw1.us.ci.rackspace.net/v3/customer_accounts/CLOUD/"+tenant_id+"/contacts?role=PRIMARY", headers=headers, verify=False)
#    root = ET.fromstring(second_r.text)#ET.parse(second_r)
#    for child in root.findall('{http://customer.api.rackspace.com/v1}contact'):
#        usersname = child.get('username')
#        return usersname
##Ssh fucked###################################################################################################################

def ssh_expect(server_number, token):
    global servers
    #servers = json.loads(servers)
    #print(servers[int(server_number)])
    #print(servers[int(server_number)]['id'])
    rack_pass = grackid(servers[int(server_number)]['id'],token)
    ssh_line = "ssh rack@"+servers[int(server_number)]['ip']+"    "+rack_pass[1:-1]
    #imp_toke = gimpuser(gusers(ddi, token), token)
    return ssh_line
    #print(gservers(ddi,imp_toke))
    #server = raw_input()
    #print(server)
 
 
###############################################################################################################################

def gservers(ddi, token):
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    datacenters = ['hkg', 'lon', 'iad', 'ord', 'syd', 'dfw']
    for dc in datacenters:    
        second_r = requests.get("https://"+dc+".servers.api.rackspacecloud.com/v2/"+ddi+"/servers", headers=headers, verify=False)
        #print(dc)
        #print(second_r)
        #print(second_r.text)
        if second_r.text:
            server_json=json.loads(second_r.text)
            #print(second_r.text)
            if server_json["servers"]:
                size = len(server_json["servers"])
                print(size)
                for i in range(size):
                    #print(i)
                #for x in xrange(1,len(server_json["servers"])):
                #print(server_json["servers"])
                #print(server_json["servers"][x])
                    global servers
                    id_name = {server_json["servers"][i]["id"]:server_json["servers"][i]["name"]}
                    servers.update(id_name)
                    print(server_json["servers"][i]["id"])
                    #print(server_id)

    #print(second_r)
    return(second_r.text)

def gcomplete(ddi, token):
    datacenters = ['hkg', 'lon', 'iad', 'ord', 'syd', 'dfw']
    admin_user = gusers(ddi,token)
    imp_token = gimpuser(admin_user, token)
    headers = {'content-type': 'application/json',"X-Auth-Token":imp_token}
    for dc in datacenters:    
        second_r = requests.get("https://"+dc+".servers.api.rackspacecloud.com/v2/"+ddi+"/servers", headers=headers, verify=False)
        if second_r.text:
            server_json=json.loads(second_r.text)
            if server_json["servers"]:
                size = len(server_json["servers"])
                print(size)
                for i in range(size):
                    global servers
                    global server_count
                    server_count += 1
                    second_r = requests.get("https://"+dc+".servers.api.rackspacecloud.com/v2/"+ddi+"/servers/"+server_json["servers"][i]["id"], headers=headers, verify=False)
                    #print(server_json)
                    if second_r.text:
                        details = json.loads(second_r.text)
                        #print(details)
                        #print(details["server"]["addresses"]["public"][0]["addr"])
                       # if i in servers.keys():
                      #      servers{'admin':admin_user,'id':server_json["servers"][i]["id"], 'name':server_json["servers"][i]["name"], 'ip':details["server"]["addresses"]["public"][0]["addr"]})
                      #  else:
                        id_name ={server_count: {'admin':admin_user,'id':server_json["servers"][i]["id"], 'name':server_json["servers"][i]["name"], 'ip':details["server"]["addresses"]["public"][0]["addr"]}}
                        servers.update(id_name)
                        print(server_json["servers"][i]["id"])

    return(servers)



def gimpuser(user_id,token):
    payload = {"RAX-AUTH:impersonation": {"user": {"username": user_id},"expire-in-seconds": 10800}}

    headers = {'content-type': 'application/json',"X-Auth-Token":token}

    second_r = requests.post("https://identity-internal.api.rackspacecloud.com/v2.0/RAX-AUTH/impersonation-tokens", data=json.dumps(payload), headers=headers)
    print(second_r.text)
    json_return = json.loads(second_r.text)
    print(json_return["access"]["token"]["id"])
    return json_return["access"]["token"]["id"]

def gtenant(token):
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    second_r = requests.get("https://identity.api.rackspacecloud.com/v2.0/tenants", headers=headers, verify=False)
    return(second_r.text)

def imp_prompt(ident,token):
	ident_p = ident + "> "
	imp_prompt = str(raw_input(ident_p))   
        if len(imp_prompt.split(' ')) ==2:
            imp_prompt,arguement = imp_prompt.split()
            if imp_prompt == "gservers":
                print(gservers(arguement,token))
        if imp_prompt == "gtenant":
            print(gtenant(token))

def help_menu():
    help_var = """
               grackid <uuid> - get rack password 
               gimpuser <username> - get impersonation token 
               gservers <ddi> - enumerate servers 
               gusers <ddi> - get admin user 
               imp <user id> - impersonation prompt 

               servers - show servers 
               tokens - show tokens 
               help - this menu 
               quit - quit """
    return(help_var)

def bye():
    exit()

#print(arg_count)
if arg_count == 3:
    command = sys.argv[1]
    arguement = sys.argv[2]
    if command == "grackid":
        grackid(arguement, racker_token)
        valid = 1
#    if command == "gimpuser":
#        new_token = gimpuser(arguement, racker_token)
#        temp_dict = {arguement:new_token}
#        global tokens
#        tokens.update(temp_dict)
#        valid = 1
    if command == "gservers":
        print(gservers(arguement, racker_token))
        valid = 1
    if command == "gusers":
        print(gusers(arguement, racker_token))
        valid = 1
    if command == "mytoken":
        print(racker_token)
        valid = 1

#    if command == "imp":
#        imp_prompt(arguement, tokens[arguement])
#        valid = 1
    if command == "ssh":
        print(ssh_expect(arguement, racker_token))
        valid = 1
    bye()	    
	
cli()


#if __name__ == '__main__':
#    threading.Thread(target=cli).start()
#    threading.Timer(2, interrupt).start()



########################################################################################
#An ssh function that you give the ddi and it gives you server names and rack shit
# ssh ddi -> gusers -> gettoken -> gservers -> menu selection -> rack password -> ssh expect
# fucking hell
########################################################################################
