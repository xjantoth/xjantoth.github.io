---
title: "Copy store.php to websupport linuxinuse.com via sftp"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=420&fit=crop"
description: "How to transfer files to a web hosting provider using scp with password authentication and sftp with a specific host key algorithm."

tags: ['ssh', 'websupport']
categories: ["Networking"]
---

Use `scp` to copy a file to a remote host with password authentication (public key disabled), or use `sftp` to connect interactively with a specific host key algorithm.

```bash
scp  -o PubkeyAuthentication=no store.php  linuxinuse.com@linuxinuse.com:web/tw/

sftp  -o HostKeyAlgorithms=ssh-rsa  devopsinuse.com@devopsinuse.com
```
