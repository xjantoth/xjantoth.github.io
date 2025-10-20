---
title: "SSH tunnel to Samba server via hron"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/ssh-1.png"
description: "SSH tunnel to Samba server via hron"

tags: ["ssh", "sabma", "hron"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

How to ''SSH'' to river

```
eval `ssh-agent`
# add SSH key to keering
ssh-add ~/.ssh/hron

ssh -A -i ~/.ssh/hron  \
tothj@hron.fei.tuke.sk  \
-t ssh jantoth@147.232.47.151

@ copy from samba to localhost :) over jumphost
scp -A -i ~/.ssh/hron -o 'ProxyJump tothj@hron.fei.tuke.sk'  jantoth@147.232.47.151:/tmp/samba.tgz .
```
