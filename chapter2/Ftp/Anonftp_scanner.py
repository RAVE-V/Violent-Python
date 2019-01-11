import ftplib

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

host='ftp.acc.umu.se'
anonLogin(host)    