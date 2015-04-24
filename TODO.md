2Proactively sanitize input

2MOVE sanitation to a seperate function

2Sanitize selector?
    sanatize Server Select

rash ddi bast server-name

rash ddi bast, then list

Sanatize input for through_bast

Api Call make image smaller

Cloud network create, assign

get-imp-token, to take ddi

Test get-ip-info, test get-ng-servers

--Change get-rack-id to get-rack-pass

create database; enable root access;


Converting arguement parsing, to ~~argparse~~ ~~getopt~~ ~~custom arg parsing~~ ok ok argparse. --Branch argparse*

I fight for the user

--Convert the ipfinder to the new naming convention, currently gipinfo.

Eliminate the current global variables in use: servers, all the ddb stuff, databases, maybe not tokens

--3Add other bastions

port number selection for ssh

--1reduce number of api calls by, only checking lon for lon and taking lon out of us (rash really needs this. the speed bump will help)

test get-databases

fix egg error

get imp-token subshell properly working

Special rules for rack connect, try this account 10043249

--Don't break on unicode named servers, might be this account 10044463

--get-rack-id to work with ip

for servers in ng_servers print server int, name ,and ip

PEP8 Consistency?


Add EOF for <ddi>

4Clean up so text for "rash <ddi>" and "rash> <ddi>" show a more user friendly selection
    Change out of JSON

5work on except script, so that it produces sudo su - and so it can better handle errors and bad connections

--tab completion

--parse https as <ddi>





*Simple argparse for reference:
```
import argparse

parser = argparse.ArgumentParser()
    parser.add_argument("a")
    args = parser.parse_args()

    if args.a == 'magic.name':
        print 'You nailed it!'
        
```
