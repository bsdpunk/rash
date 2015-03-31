def ssh(name, loginInfo):
#    '''
#    ssh into managed cloud server using /usr/bin/env expect
#    '''
#    autorun_script_path=os.path.expanduser('~/.config/hammercloud/autorun')
#    autorund_script_path='{0}.d'.format(autorun_script_path)
#    if not loginInfo['admin_password']:
#        raise Exception('Unmanaged Cloud Server: no rack password')
#    GREEN = re.escape('\033[92m')
#    RESET = re.escape('\033[0m')
#    RED = re.escape('\033[91m')
#    YELLOW = re.escape('\033[93m')
#    WHITE = re.escape('\033[97m')
#    CYAN = re.escape('\033[96m')
#    PINK = re.escape('\033[95m')
#    BLUE = re.escape('\033[94m')

    output = []

    output.append('#!/usr/bin/env expect\n')

    loginInfo['admin_password'] = re.escape(loginInfo['admin_password'])

#    output.append('proc serverinfo {} {\n')
#    output.append('send_user "{0}Device:{1} {2}\n'.format(BLUE, RESET, name))
#    output.append('{0}UUID:{1} {2}\n'.format(BLUE, RESET, loginInfo['uuid']))
#    output.append('{0}Account:{1} {2}\n'.format(BLUE, RESET, loginInfo['ddi']))
#    output.append('{0}Primary IP:{1} {2}\n'.format(BLUE, RESET, loginInfo['ip']))
#    if loginInfo['rackconnect'] is 2:
#        output.append('{0}Initial Public IP: {1} {2}\n'.format(BLUE, RESET, loginInfo['public_ip']))
#    output.append('{0}Private IP:{1} {2}\n'.format(BLUE, RESET, loginInfo['private_ip']))
#    output.append('{0}User:{1} {2} / {3}\n'.format(BLUE, RESET, loginInfo['username'], loginInfo['admin_password']))
#    output.append('\n"}\n')
#    output.append('serverinfo\n')

#    output.append('exec rm -f $argv0\n')
#    output.append('set timeout -1\n')
#    output.append('log_user 1\n')
#    loginip = loginInfo['private_ip'] if loginInfo['rackconnect'] is 3 or loginInfo['use_private'] else loginInfo['ip']
#    if loginInfo['rackconnect'] is 3:
#        if loginInfo['ssh_key']:
#            ProxyCommand = "ssh -a {sso}@{bastion} -i {ssh_key} 'nc -w 900 %h %p'"
#        else:
#            ProxyCommand = "ssh -a {sso}@{bastion} 'nc -w 900 %h %p'"
#        loginInfo['ssh_args'] += ' -o "ProxyCommand {cmd}" '.format(cmd=ProxyCommand.format(
#            bastion=DCS[loginInfo['dc'].upper()],
#            ssh_key=loginInfo['ssh_key'],
#            sso=loginInfo['sso']
#        ))

    output.append(('spawn -noecho ssh -l rack -o PubkeyAuthentication=no '
        '-o RSAAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
        '-o GSSAPIAuthentication=no '+ pub_ip +' -p {port} {ssh_args}\n').format(loginip=loginip, **loginInfo))
    output.append('match_max 100000\n')

#    if loginInfo['rackconnect'] is 3 and not loginInfo['ssh_key']:
#        rsatoken = getpass.getpass('RSA + PIN: ').strip()
#        output.append('expect {\n')
#        output.append('\t-re {Enter PASSCODE:} {\n')
#        output.append('\t\tsleep .1\n')
#        output.append('\t\tsend -- "{rsatoken}\r"\n'.format(rsatoken=rsatoken))
#        output.append('\t\tsleep .1\n')
#        output.append('\t}\n')
#        output.append('}\n');

    output.append('expect {\n')
    output.append('\t-re {[P|p]assword: } {\n')
    output.append('\t\tsleep .1\n')
    output.append('\t\tsend -- "'+password+'\r"\n'.format(**loginInfo))
    output.append('\t\tsleep .1\n')
    output.append('\t}\n')
    output.append('\t"Connection closed by remote host" {\n')
    output.append('\t\texit\n')
    output.append('\t}\n')
    output.append('\t-re "\]. |incorrect password|sudoers|try again|root|ROOT|%% "\n')
    output.append('}\n');

#    if loginInfo['skip_root'] is False:
#        output.append('expect {\n')
#        output.append('\t-re "\$|\$:" {\n')
#        output.append('\t\tsend -- "LC_ALL=en exec sudo -k su - ;\r"\n')
#        output.append('\t\tsleep .1\n')
#        output.append('\t}\n')
#        output.append('}\n')

    output.append('trap { stty rows [stty rows] columns [stty columns] < $spawn_out(slave,name)} WINCH\n')

#    if not loginInfo['skip_scripts'] and os.path.exists(autorun_script_path):
#        output.append('expect {\n')
#        output.append('\t-re "\$|\$:" {\n')
#        with open(autorun_script_path, 'r') as autorun_script:
#            line_command = re.escape(
#                "; ".join([line.rstrip() for line in
#                           autorun_script.readlines()]))
        output.append('\t\tsend -- "{0}\r"\n'.format(line_command))
        output.append('\t\tsleep .1\n')
        output.append('\t}\n')
        output.append('}\n')
#    if not loginInfo['skip_scripts'] and os.path.exists(autorund_script_path):
#        for scriptfile in sorted(os.listdir(autorund_script_path)):
#            output.append('expect {\n')
#            output.append('\t-re "\$|\$:" {\n')
#            with open(os.path.join(autorund_script_path, scriptfile), 'r') as autorund_script:
#                line_command = re.escape(
#                    "; ".join([line.rstrip() for line in
#                               autorund_script.readlines()]))
#            output.append('\t\tsend -- "{0}\r"\n'.format(line_command))
#            output.append('\t\tsleep .1\n')
#            output.append('\t}\n')
#            output.append('}\n')

    output.append('interact {\n')
    output.append('\t\\034 exit\n')
    output.append('}\n')

#    confdir = '{0}/.rashscript'.format(os.path.expanduser('~'))
#    script_path = '{0}/{1}.sh'.format(confdir, name)
#    fh = open(script_path, 'w')
#    fh.write("".join(output))
#    fh.close()
#    os.chmod(script_path, 448)

    subprocess.call(script_path)
    #sys.exit(0)


