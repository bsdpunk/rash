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
