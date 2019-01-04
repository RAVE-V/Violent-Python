import optparse
from pexpect import pxssh

class clientClass:

    def __init__(self,host,user,password):
        self.host=host
        self.user=user
        self.password=password
        self.session=self.connect()

    def connect(self):
        try:
            s=pxssh.pxssh()
            s.login(self,self.user,self.user,self.password)
            return s
        except Exception,e:
            print (e)
            print('[-] Error Connecting')
    
    def send_command(self,cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

def add_client(host,user,password):
    client=clientClass(user,host,password)
    botNet.append(client)

def botnetCommand(command):
    for client in botNet:
        out=client.send_command(command)
        print('[*] Output from '+client.host)
        print('[+] '+output+'\n')

botNet=[]
add_client('s3.sshservers.us','data-freevpn.us','pass')
botnetCommand('uname -v')