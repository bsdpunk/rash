Proactively sanitize input
Converting arguement parsing, to ~~argparse~~ ~~getopt~~ ~~custom arg parsing~~ ok ok argparse. --Branch argparse*
--Convert the ipfinder to the new naming convention, currently gipinfo.
Eliminate the current global variables in use: servers, databases, maybe not tokens
Add other bastions
port number selection for ssh
reduce number of api calls by, only checking lon for lon and taking lon out of us (rash really needs this. the speed bump will help)
test get-databases
get imp-token subshell properly working
Don't break on unicode named servers
--get-rack-id to work with ip
for servers in ng_servers print server int, name ,and ip


Add EOF for <ddi>
Clean up so text for "rash <ddi>" and "rash> <ddi>" show a more user friendly selection
work on except script, so that it produces sudo su - and so it can better handle errors and bad connections
tab completion

parse https as <ddi>





*Simple argparse for reference:
```
import argparse

parser = argparse.ArgumentParser()
    parser.add_argument("a")
    args = parser.parse_args()

    if args.a == 'magic.name':
        print 'You nailed it!'
        
```
