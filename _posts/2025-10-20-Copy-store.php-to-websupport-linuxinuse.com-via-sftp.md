---
title: "Copy store.php to websupport linuxinuse.com via sftp"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=420&fit=crop"
description: "Copy store.php to websupport linuxinuse.com via sftp — practical walkthrough with examples."

tags: ['ssh', 'websupport']
categories: ["Networking"]
---

```
scp  -o PubkeyAuthentication=no store.php  linuxinuse.com@linuxinuse.com:web/tw/

sftp  -o HostKeyAlgorithms=ssh-rsa  devopsinuse.com@devopsinuse.com
```
