---
title: "Linux Capabilities"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
description: "You cannot change system time even though you are not using APPARMOR or SECCOMP. There is something called ''linux capabilities'' to make granular group to execute."

tags: ['linux', 'capabilities']
categories: ["Linux"]
---

You cannot change system time even though you are not using APPARMOR or SECCOMP.
There is something called ''linux capabilities'' to make granular group to execute ''privileged action''.


```
getcap /usr/bin/ping
ps -ef | grep sshd

getcap <process-id-of-sshd>
```
