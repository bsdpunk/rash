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
In the future rash will support the creation of this file as well as, a passwordless version. 
```

Commands:

```
grackid <uuid> - get rack password 
gimpuser <username> - get impersonation token 
gnextservers <ddi> - enumerate next gen servers, standard servers included
guser <ddi> - get admin user 
imp <user id> - impersonation prompt
gtoken - refresh your token
gdbinstances or gdbin - enumerate database instances 

<ddi> - display servers, select a server, select a bastion, then it will ssh through the bastion to the server
servers - show servers 
tokens - show tokens
mytoken - show your token 
help - this menu 
quit - quit 
```
