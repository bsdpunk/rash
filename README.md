# Installing
You must have expect installed for the ssh functions to work.
To install untar, and use the python install.

```
tar -xvf rash.tar.gz
cd rash
sudo python setup.py install 
```

# Use
Before you can use rash, you need to be on the rackspace network, as the first thing it does is, authenticates you, then grabs your rackspace token. 

A .rash will be made in your home directory that will hold your credentials. 
### Example:

```
{ "default":[{ "username":"yourusername", "password":"yourpassword" }] } 
```

Commands:

```
get-rack-id <uuid> - get rack password 
get-imp-token <username> - get impersonation token 
get-ng-servers <ddi> - enumerate next gen servers, standard servers included
get-user <ddi> - get admin user 
prompt-imp <user id> - impersonation prompt, Hella alpha
get-token - refresh your token
get-db-instances - enumerate database instances , hella beta
get-ip-info - Get the ip information from ipfinder, hella beta

<ddi> - display servers, select a server, select a bastion, then it will ssh through the bastion to the server
<https url in cloud control> - display servers, select a server, select a bastion, then it will ssh through the bastion to the server
servers - show servers 
tokens - show tokens
mytoken - show your token 
help - this menu 
quit - quit 
```
