---
title: "Keep SSH active"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=420&fit=crop"
description: "**Make this part of your SSH config file''."

tags: ['ssh', 'active']
categories: ["Networking"]
---

**Make this part of your SSH config file''

```
worker ~ $ cat ~/.ssh/config
Host *
    ServerAliveInterval 60
    AddressFamily inet

```
