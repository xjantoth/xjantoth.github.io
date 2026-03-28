---
title: "Remove tiddlywiki backup files from websupport"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=420&fit=crop"
description: "Use SFTP with regular expressions to bulk-remove TiddlyWiki backup files from a web hosting server."

tags: ['ssh', 'tiddlywiki']
categories: ["Networking"]
---

This first example removes a single TiddlyWiki backup file via SFTP using a heredoc to automate the session.

```bash
sftp linuxinuse.com@linuxinuse.com << EOF
rm web/tw/index.20200430.153755.html
exit
EOF
```

**Take advantage of regular expressions.** Instead of deleting backup files one by one, use a glob pattern to match all timestamped backup files at once.

```bash
sftp linuxinuse.com@linuxinuse.com << EOF
rm  web/tw/index.[0-9\.]*.html
exit
EOF

```
