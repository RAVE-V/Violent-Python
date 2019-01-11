import pexpect
prompt=['#','>>>','>','\$']

def send_command(child,cmd):
    child.sendline('')
    child.sendline('')
    child.sendline('')
    child.expect('sdf:/sdf/udd/q/qwer1234qw>')
    child.sendline(cmd)
    child.expect(prompt)
    print(child.before)

def connect(user,host,password):
    ssh_newkey='Are you sure you want to continue connecting'
    connstr='ssh '+ user + '@' + host
    child=pexpect.spawn(connstr)
    ret= child.expect([pexpect.TIMEOUT,ssh_newkey,'[P|p]assword'])
    if ret==0:
        print('[-] Error Connecting')
        return
    if ret==1:
        child.sendline('yes')
        ret=child.expect([pexpect.TIMEOUT,'[P|p]assword'])
        if ret==0:
            print('[-] Something is Wrong')
            return
    if ret==2:
        child.sendline(password)
        child.expect(prompt)
        return child

def main():
    host='tty.sdf.org'
    user='qwer1234qw'
    password='1FAmI4MepsqV6w'
    child=connect(user,host,password)
    send_command(child,'ls')

if __name__=='__main__':
    main()
