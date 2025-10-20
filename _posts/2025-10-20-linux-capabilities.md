---
title: "Linux Capabilities"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Linux Capabilities"

tags: ['linux', 'capabilities']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

You cannot change system time even though you are not using APPARMOR or SECCOMP.
There is something called ''linux capabilities'' to make granular group to execute ''privileged action''.


```
getcap /usr/bin/ping
ps -ef | grep sshd

getcap <process-id-of-sshd>
```
