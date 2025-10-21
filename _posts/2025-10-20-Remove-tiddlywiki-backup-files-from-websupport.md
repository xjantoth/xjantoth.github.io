---
title: "Remove tiddlywiki backup files from websupport"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/ssh-1.png"
description: "Remove tiddlywiki backup files from websupport"

tags: ['ssh', 'tiddlywiki']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
sftp linuxinuse.com@linuxinuse.com << EOF
rm web/tw/index.20200430.153755.html
exit
EOF
```
Take an advantage of ''regular expressions''

```
sftp linuxinuse.com@linuxinuse.com << EOF
rm  web/tw/index.[0-9\.]*.html
exit
EOF

```
