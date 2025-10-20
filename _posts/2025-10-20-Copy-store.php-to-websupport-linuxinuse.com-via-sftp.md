---
title: "Copy store.php to websupport linuxinuse.com via sftp"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/ssh-1.png"
description: "Copy store.php to websupport linuxinuse.com via sftp"

tags: ['ssh', 'websupport']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
scp  -o PubkeyAuthentication=no store.php  linuxinuse.com@linuxinuse.com:web/tw/

sftp  -o HostKeyAlgorithms=ssh-rsa  devopsinuse.com@devopsinuse.com
```
