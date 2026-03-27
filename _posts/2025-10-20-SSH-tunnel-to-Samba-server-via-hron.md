---
title: "SSH tunnel to Samba server via hron"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=420&fit=crop"
description: "How to ''SSH'' to river."

tags: ['ssh', 'sabma', 'hron']
categories: ["Networking"]
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
