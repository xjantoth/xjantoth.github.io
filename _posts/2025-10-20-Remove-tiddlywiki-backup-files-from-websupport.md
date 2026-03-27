---
title: "Remove tiddlywiki backup files from websupport"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=420&fit=crop"
description: "Take an advantage of ''regular expressions''."

tags: ['ssh', 'tiddlywiki']
categories: ["Networking"]
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
