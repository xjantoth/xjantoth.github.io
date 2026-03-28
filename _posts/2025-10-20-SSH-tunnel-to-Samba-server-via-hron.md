---
title: "SSH tunnel to Samba server via hron"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=420&fit=crop"
description: "How to SSH through a jump host (hron) to reach a Samba server, including SCP file copy over the tunnel."

tags: ['ssh', 'sabma', 'hron']
categories: ["Networking"]
---

## How to SSH to Samba server via hron

This example demonstrates how to use SSH agent forwarding and a jump host to reach a remote Samba server. It also shows how to copy files from the Samba server to your local machine through the jump host using SCP with the ProxyJump option.

```bash
eval `ssh-agent`
# add SSH key to keyring
ssh-add ~/.ssh/hron

ssh -A -i ~/.ssh/hron  \
tothj@hron.fei.tuke.sk  \
-t ssh jantoth@147.232.47.151

# copy from samba to localhost over jumphost
scp -A -i ~/.ssh/hron -o 'ProxyJump tothj@hron.fei.tuke.sk'  jantoth@147.232.47.151:/tmp/samba.tgz .
```
