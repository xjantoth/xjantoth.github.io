---
title: "Keep SSH active"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/ssh-1.png"
description: "Keep SSH active"

tags: ['ssh', 'keep', 'active']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

**Make this part of your SSH config file''

```
worker ~ $ cat ~/.ssh/config
Host *
    ServerAliveInterval 60
    AddressFamily inet

```
