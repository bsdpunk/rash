import re
import os
import subprocess

def ssh(pub_ip, password):

    output = []

    output.append('#!/usr/bin/env expect\n')

    #loginInfo['admin_password'] = re.escape(loginInfo['admin_password'])
    output.append('spawn -noecho ssh -l rack -o PubkeyAuthentication=no '
        '-o RSAAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
        '-o GSSAPIAuthentication=no '+ pub_ip +'\n')
    output.append('match_max 100000\n')

    output.append('expect {\n')
    output.append('\t-re {[P|p]assword: } {\n')
    output.append('\t\tsleep .1\n')
    #print(password)
    output.append('\t\tsend -- "'+password+'\r"\n')
    output.append('\t\tsleep .1\n')
    output.append('\t}\n')
    output.append('\t"Connection closed by remote host" {\n')
    output.append('\t\texit\n')
    output.append('\t}\n')
    output.append('\t-re "\]. |incorrect password|sudoers|try again|root|ROOT|%% "\n')
    output.append('}\n');

    output.append('trap { stty rows [stty rows] columns [stty columns] < $spawn_out(slave,name)} WINCH\n')

    output.append('interact {\n')
    output.append('\t\\034 exit\n')
    output.append('}\n')
    
    name = 'rash'
    confdir = '{0}'.format(os.path.expanduser('~'))
    script_path = '{0}/{1}.sh'.format(confdir, name)
    fh = open(script_path, 'w')
    fh.write("".join(output))
    fh.close()
    os.chmod(script_path, 448)


    subprocess.call(script_path)
