#!/usr/bin/python3
from subprocess import check_output
import json


FLAG = '3k{jq_is_r3ally_HelpFULL_3af4bcd97f5}'

def help():
	print('''.help\t\t\tPrint this help
.version\t\tPrint versions
.search\t\t\tSearch libcdb 
.secret\t\t\tPrint flag
''')

def sanitize(kstr):
	return kstr.replace('(','').replace(')','')


print('Login    > ', end='')
uLogin = input()
print('Password > ', end='')
uPassw = input()

if(not uLogin.isalnum() or not uPassw.isalnum()):
	exit('login/passw only alphanumeric')

cmdArg1='. as $maindb | .users[] | select(.username=="'+uLogin+'") | select(.password=="'+(uPassw)+'") '
resp=check_output(["jq","-c", cmdArg1, 'maindb.json']).decode('utf8')



try:
	thisLogin = json.loads(resp.strip())
	print('Authenticated {"users":', end='')
	print(resp.strip(), end='')
	print("}")
	if(not uLogin==thisLogin['username'] or not uPassw==thisLogin['password']):
		exit('login failed')
except Exception as e:
	exit('login failed')


print('''                            
 __    _ _       ____  _____ 
|  |  |_| |_ ___|    \\| __  |
|  |__| | . |  _|  |  | __ -|
|_____|_|___|___|____/|_____|
                         as a service


Type .help for help


''')




while(True):
	print('> ', end='')
	uInput = input()
	if(uInput.startswith('.help') ):
		help()
	elif(uInput.startswith('.version') ):
		print('''"ubuntu_libc6-dbg_2.4-1ubuntu12.3_amd64"
"ubuntu_libc6-dbg_2.4-1ubuntu12_amd64"
"ubuntu_libc6-i386_2.10.1-0ubuntu15_amd64"
			''')
	elif(uInput.startswith('.search') ):
		csymbol,caddress,cfilter= None,None,None
		cmdArgs = uInput.split(' ')
		if(len(cmdArgs)>=3):
			csymbol  = sanitize(cmdArgs[1])
			caddress = sanitize(cmdArgs[2])
		if(len(cmdArgs)>=4):
			cfilter = sanitize(cmdArgs[3])
		else:
			cfilter=''
		if(csymbol is None or caddress is None):
			print('.search <*symbol> <*addr> <filter>\nEx: .search fprintf 0x4b970\n\n* required field\n')
		else:
			try:
				caddress=int(caddress,16) & 0xfffff
			except Exception as e:
				print('invalid address')
				break
			cmdArg1='. as $maindb | .libcDB[] | select(.symbol=="'+csymbol+'") | select(.address|contains("'+str(caddress)+'")) | .'+cfilter
			try:
				Out = check_output(["jq","-c", cmdArg1, 'maindb.json'])
				for thisLine in Out.decode('utf8').split('\n'):
					if thisLine is not ''  and thisLine != 'null':
						thisQuery = json.loads(thisLine.strip())
						if(thisQuery is not None):
							print('Found:')
							if("id" in thisQuery):
								print("\tid\t\t"+thisQuery['id'])
							if("name" in thisQuery):
								print("\tname\t\t"+thisQuery['name'])
							if("symbol" in thisQuery):
								print("\tsymbol\t\t"+thisQuery['symbol'])
							if("address" in thisQuery):
								print("\taddress\t\t"+hex(int(thisQuery['address'])))
						else:
							print(thisLine)
							break
			except Exception as e:
				ffa=11
	elif(uInput.startswith('.secret') ):
		if(uLogin!='admin'):
			print('not admin\nno flag for u')
		else:
			print(FLAG)