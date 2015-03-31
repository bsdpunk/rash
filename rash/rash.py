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
import signal
#from pexpect import pxssh
import random
import getpass
import urlparse
#import spur
import ssh_script

#sys.path.append('/home/dust7955/rash0.81/rash0.81/rash0.81/lib/python2.7/site-packages/pexpect/pexpect')
#from pexpect import *
#Counters and Toggles
arg_count = 0
no_auth = 0
server_count = 0
database_count = 0
hist_toggle = 0
prompt_r = 0

for arg in sys.argv:
    arg_count += 1

#warnings are ignored because of unverified ssl warnings which could ruin output for scripting
import warnings
warnings.filterwarnings("ignore")



#These are lists of things that are persistent throughout the session
tokens = {}
servers = {}
databases = {}





#os expand must be used for 
config_file = os.path.expanduser('~/.rash')
hist_file = os.path.expanduser('~/.rash_history')

hfile = open(hist_file, "a")
if os.path.isfile(config_file):
    config=open(config_file, 'r')
    config=json.load(config)
else:
    username = raw_input("Username:")
    password = getpass.getpass("Password:")
    config= {"default":[{"username":username,"password":password}]}
    
    config_file_new = open(config_file, "w")
    config_f = str(config)
    config_f = re.sub("'",'"',config_f)
    config_file_new.write(config_f)
    config_file_new.close() 

#Ending when intercepting a KeyboardInterrupt
def Exit_gracefully(signal, frame):
    sys.exit(0)


def get_racker_token(config):
    signal.signal(signal.SIGINT, Exit_gracefully)

    username = config["default"][0]["username"]
    password = config["default"][0]["password"]

    headers = {'content-type': 'application/json'}
    payload = {"auth":{"RAX-AUTH:domain":{"name":"Rackspace"},"passwordCredentials":{"username":username,"password":password}}}
    r = requests.post("https://identity-internal.api.rackspacecloud.com/v2.0/tokens", data=json.dumps(payload), headers=headers)
    json_data = json.loads(r.text)
    try:
        racker_token = json_data["access"]["token"]["id"]
    except KeyError:
        print("Bad Credentials!")
        os.unlink(config_file)
        bye()
    return(racker_token)

rash_p = 'rash'


def cli():
    while True:
        valid = 0

        signal.signal(signal.SIGINT, Exit_gracefully)
        cli = str(raw_input(PROMPT))
        if hist_toggle == 1:
            hfile.write(cli + '\n')

#This is not just a horrible way to take the commands and arguements, it's also shitty way to sanatize the input for one specific scenario
#I miss perl :(
        cli = re.sub('  ',' ', cli.rstrip())
        if len(cli.split(' ')) ==2:
            command,arguement = cli.split()
            if command == "grackid":
                print(grackid(arguement, racker_token))
                valid = 1
            if command == "gimpuser":
                new_token = gimpuser(arguement, racker_token)
                temp_dict = {arguement:new_token}
                print(new_token)
                global tokens
                tokens.update(temp_dict)
                valid = 1
            if command == "gservers":
                print(gservers(arguement, racker_token))
                valid = 1
            if command == "goldservers" or command == "gold":
                goldservers(arguement, racker_token)
                #pprint(servers)
                valid = 1 
            if command == "gipinfo":
                pprint(gipinfo(arguement, racker_token))
                valid = 1 
            if command == "gnextservers" or command == "gnservers":
                gnextservers(arguement, racker_token)
                pprint(servers)
                valid = 1 
            if command == "gdbinstances" or command == "gdbin":
                gdbinstances(arguement, racker_token)
                pprint(databases)
                valid = 1 
            if command == "guser":        
                print(guser(arguement, racker_token))
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
        if cli == "databases":
            pprint(databases)
            valid = 1
        if cli == "tokens":
            pprint(tokens)
            valid = 1
        if cli == "quit" or cli == "exit":
            hfile.close()
            bye()
        if cli == "help":
            print(help_menu())
            valid = 1
        if cli == "mytoken":
            print(racker_token)
            valid = 1
        if cli == "gtoken":
            print(get_racker_token(config))
            valid = 1
	

        if valid == 0:
            print("Unrecoginized Command")

def grackid(uuid,token):
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    second_r = requests.get("https://passwords.servermill.rackspace.net/v1/"+uuid+"/password/current", headers=headers)
    rack_pass=second_r.text
    rack_pass=rack_pass[1:-1]
    return(rack_pass)


def gipinfo(ip,token):
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    second_r = requests.get("https://ipfinder.rackspace.com/json/"+ip, headers=headers, verify=False)
    ip_info=second_r.text
    return(ip_info)




def guser(tenant_id,token):
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    second_r = requests.get("https://customer-admin.prod.dfw1.us.ci.rackspace.net/v3/customer_accounts/CLOUD/"+tenant_id+"/contacts?role=PRIMARY", headers=headers, verify=False)
    root = ET.fromstring(second_r.text)#ET.parse(second_r)
    for child in root.findall('{http://customer.api.rackspace.com/v1}contact'):
        usersname = child.get('username')
        return usersname

##Ssh fucked###################################################################################################################

def ssh_expect(server_number, token):
    global servers
    #print(server_number)
    #print(server_count)
    try:
        server_number = int(server_number)
    except ValueError:
        pass
    if isinstance( server_number, (int) ) and server_count >= server_number:
        rack_pass = grackid(servers[int(server_number)]['id'],token)
        ssh_line = "ssh rack@"+servers[int(server_number)]['ip']+"    "+rack_pass[1:-1]
        
        ip = servers[int(server_number)]['ip']
#       username = 'rack'
        password = rack_pass
        #print(password) 
        ssh_script.ssh(ip, password)
        return ssh_line
    else: 
        print("This is not a valid option")
###This needs to verify that it's an ipv4 address, via JSON not regex...I implimented this a different way somewhere else need to swap it out...maybe an old version lost due to careless version contorl....hmmmm 
###I was just going to throw this to a shell with pexpect, but I'm fucking tired, maybe tomorrow 
###############################################################################################################################

###If you want to know why this function exists you'll have to ask me in person
def gservers(ddi, token):
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    datacenters = ['hkg', 'lon', 'iad', 'ord', 'syd', 'dfw']
    for dc in datacenters:    
        second_r = requests.get("https://"+dc+".servers.api.rackspacecloud.com/v2/"+ddi+"/servers", headers=headers, verify=False)
        if second_r.text:
            server_json=json.loads(second_r.text)
            if server_json["servers"]:
                size = len(server_json["servers"])
                print(size)
                for i in range(size):
                    global servers
                    id_name = {server_json["servers"][i]["id"]:server_json["servers"][i]["name"]}
                    servers.update(id_name)
                    print(server_json["servers"][i]["id"])
    return(second_r.text)
#############################################################################################################################


def gnextservers(ddi, token):
    datacenters = ['hkg', 'lon', 'iad', 'ord', 'syd', 'dfw']
    admin_user = guser(ddi,token)
    if admin_user == None:
        return(admin_user)
    imp_token = gimpuser(admin_user, token)
    headers = {'content-type': 'application/json',"X-Auth-Token":imp_token}
    for dc in datacenters:    
        second_r = requests.get("https://"+dc+".servers.api.rackspacecloud.com/v2/"+ddi+"/servers", headers=headers, verify=False)
        if second_r.text:
            server_json=json.loads(second_r.text)
            if server_json["servers"]:
                size = len(server_json["servers"])
                #print(size)
                for i in range(size):
                    global servers
                    global server_count
                    server_count += 1
                    second_r = requests.get("https://"+dc+".servers.api.rackspacecloud.com/v2/"+ddi+"/servers/"+server_json["servers"][i]["id"], headers=headers, verify=False)
                    #print(server_json)
                    if second_r.text:
                        details = json.loads(second_r.text)
                        #print(details)
#Probably should add the fucking type of server, dolt
#Probably should add a lot of things, need input from others
                        size_ip = len(details["server"]["addresses"]["public"])
                        #print(size_ip)
                        for ip in range(size_ip):
                            #print(i)
                        
                            if str(details["server"]["addresses"]["public"][ip]["version"]) == "4":
                                pub_ip = details["server"]["addresses"]["public"][ip]["addr"]
                        
                        if pub_ip:         
                            id_name ={server_count: {'admin':admin_user,'ddi':ddi,'id':str(server_json["servers"][i]["id"]), 'name':str(server_json["servers"][i]["name"]), 'ip':str(pub_ip)}}
                            servers.update(id_name)
                        else:
                            print("A server did not report an IPv4 address")
                            print(details["server"])
    return(servers)
#########################


############################Standard Servers, old servers whatever############

def goldservers(ddi, token):
    datacenters = ['hkg', 'lon', 'iad', 'ord', 'syd', 'dfw']
    admin_user = guser(ddi,token)
    if admin_user == None:
        return(admin_user)
    imp_token = gimpuser(admin_user, token)
    headers = {'content-type': 'application/json',"X-Auth-Token":imp_token}
    #for dc in datacenters:    
    second_r = requests.get("https://servers.api.rackspacecloud.com/v1.0/"+ddi+"/servers/detail", headers=headers, verify=False)
    if second_r.text:
        print(second_r.text)
    return(servers)


#####As of right now I'm not going to document this, it's hella untested
def gdbinstances(ddi, token):
    datacenters = ['hkg', 'lon', 'iad', 'ord', 'syd', 'dfw']
    admin_user = guser(ddi,token)
    if admin_user == None:
        return(admin_user)
    imp_token = gimpuser(admin_user, token)
    headers = {'content-type': 'application/json',"X-Auth-Token":imp_token}
    for dc in datacenters:    
        second_r = requests.get("https://"+dc+".databases.api.rackspacecloud.com/v1.0/"+ddi+"/instances", headers=headers, verify=False)
        if second_r.text:
            db_json=json.loads(second_r.text)
            #print(db_json)
            if db_json["instances"]:
                size = len(db_json["instances"])
                #print(size)
                for i in range(size):
                    global databases
                    global database_count
                    database_count += 1	
                    #This is so broken
                    print(db_json["instances"])

                    id_name ={database_count: {'admin':admin_user,'ddi':ddi,'name':str(db_json["instances"][i]["name"]), 'status':str(db_json["instances"][i]["status"]),'hostname':str(db_json["instances"][i]["hostname"]),'id':str(db_json["instances"][i]['id']),'size':str(db_json["instances"][i]["volume"]['size']),'size':str(db_json["instances"][i]["datastore"]["type"])}}
                    
                    databases.update(id_name)
                        #print(server_json["servers"][i]["id"])

    return(db_json)


def gimpuser(user_id,token):
    payload = {"RAX-AUTH:impersonation": {"user": {"username": user_id},"expire-in-seconds": 10800}}
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    second_r = requests.post("https://identity-internal.api.rackspacecloud.com/v2.0/RAX-AUTH/impersonation-tokens", data=json.dumps(payload), headers=headers)
    json_return = json.loads(second_r.text)
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
                print(gnextservers(arguement,token))
        if imp_prompt == "gtenant":
            print(gtenant(token))

def help_menu():
####Why did I space the help like this, cause something something, then lazy
    help_var = """
grackid <uuid> - get rack password 
gimpuser <username> - get impersonation token 
gnextservers <ddi> - enumerate next gen servers, standard servers included
guser <ddi> - get admin user 
imp <user id> - impersonation prompt
gtoken - refresh your token
gdbinstances or gdbin - enumerate database instances 

servers - show servers 
tokens - show tokens
mytoken - show your token 
help - this menu 
quit - quit """
    return(help_var)

def bye():
    exit()


if arg_count == 2:
    command = sys.argv[1]
#noauth is essentially for testing
    if command == "noauth":
        no_auth = 1
#history is to toggle writing a history file, there is currently no clean up so it is off by default
    if command == "history":
        hist_toggle = 1
    if command == "roulette":
        rando = random.randint(1, 3)
    if command == "extra":
        rash_p = config["default"][0]["prompt"]
    if command.isdigit():
        if no_auth == 1:
            racker_token =0
        else:
            racker_token = get_racker_token(config)
        gnextservers(command, racker_token)
        pprint(servers)
        server_choice = raw_input("Which Server > ")
        ssh_expect(int(server_choice),racker_token)





PROMPT = rash_p + '> '

if no_auth == 1:
    racker_token =0
else:
    racker_token = get_racker_token(config)

####Again, shit way to do this, Here's hoping it's better in beta :)
    ##You know what, fuck you, it's fine
if arg_count == 3:
    command = sys.argv[1]
    arguement = sys.argv[2]
    if command == "gipinfo":
        pprint(gipinfo(arguement, racker_token))
        valid = 1
    if command == "grackid":
        print(grackid(arguement, racker_token))
        valid = 1
    if command == "gimpuser":
        print(gimpuser(arguement, racker_token))
        valid = 1
    if command == "gservers":
        print(gservers(arguement, racker_token))
        valid = 1
    if command == "gnextservers" or command =="gnservers":
        gnextservers(arguement, racker_token)
        pprint(servers)
        valid = 1
    if command == "gdbinstances" or command == "gdbin":
        gdbinstances(arguement, racker_token)
        pprint(databases)
        valid = 1 
    if command == "guser":
        print(guser(arguement, racker_token))
        valid = 1
    if command == "mytoken":
        print(racker_token)
        valid = 1
    if command == "ssh":
        print(ssh_expect(arguement, racker_token))
        valid = 1
#    if command == 
    bye()	    

#	if __name__ == '__main__':
#    threading.Thread(target=cli).start()
#    threading.Timer(2, interrupt).start()


########################################################################################
#An ssh function that you give the ddi and it gives you server names and rack shit
# ssh ddi -> guser -> gettoken -> gservers -> menu selection -> rack password -> ssh expect
# fucking hell
########################################################################################
