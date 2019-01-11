import optparse
import sys
from threading import Thread
import threading
import socket
from socket import *

def main():
    parser= optparse.OptionParser('usage:python portmon.py-H <target host> -p <target port>')
    parser.add_option('-H',dest='tgthost',type='string',help='Specify target ip address')
    parser.add_option('-p',dest='tgtport',type='string',help='Specify target port')
    (options,args)=parser.parse_args()
    tgthost=options.tgthost
    tgtport=options.tgtport
    if (tgthost == None) | (tgtport == None):
        print parser.usage
        exit(0)
    tgtport=tgtport.split(',')
    portScan(tgthost,tgtport)
screenlock=threading.Semaphore(value=1)
def connScan(tgthost,tgtport):
    try:
        conns=socket(AF_INET,SOCK_STREAM)
        conns.connect((tgthost,tgtport))
        conns.send('ravi\r\n')
        result=conns.recv(100)
        screenlock.acquire()
        print("[+] %d TCP open"%tgtport)
        print('[+] '+ str(result))
        conns.close()
    except:
        screenlock.acquire()
        print('[-] %d TCP closed'%tgtport)
    finally:
        screenlock.release()
        conns.close()


def portScan(tgthost,tgtport):
    try:
        tgtip=gethostbyname(tgthost)
    except:
        print('[-] Cannnot resolve %s : Unknown host'%tgthost)
        return

    try:
        tgtname=gethostbyaddr(tgtip)
        print('\n SCAN RESULT : ' + tgtname[0])
    except:
        print('\n SCAN RESULT : ' + tgtip)
    setdefaulttimeout(1)
    for TgtPort in tgtport:
        print('\nScanning port ' +TgtPort)
        t= Thread(target=connScan,args=(tgthost,int(TgtPort)))
        t.start()
        #connScan(tgthost,int(TgtPort))

if __name__=='__main__':
        main()
