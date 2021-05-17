```
Emoji - 438pts - 25 solves - Author: rekter0

browse some emojis

Challenge



First Blood
1. Never Stop Exploiting
2. ISITDTU
3. Black Bauhinia
```

Emoji was simple
first vuln here,
```
		function fetch_and_parse($page){
                $a=file_get_contents("https://raw.githubusercontent.com/3kctf2021webchallenge/downloader/master/".$page.".html");
                preg_match_all("/<img src=\"(.*?)\">/", $a,$ma);
                return $ma;
        }
```
create a repo with html file containing payload for the RCE in img tag $d = "bash -c \"curl -o /dev/null ".escapeshellarg("https://raw.githubusercontent.com/3kctf2021webchallenge/downloader/master/".$url)."  \""; and navigate to it through path traversal so you can forge signature for your payload