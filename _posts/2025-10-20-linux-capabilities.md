---
title: "Linux Capabilities"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
description: "Linux capabilities allow fine-grained control over privileged operations without granting full root access, complementing AppArmor and seccomp."

tags: ['linux', 'capabilities']
categories: ["Linux"]
---

You cannot change system time even though you are not using AppArmor or seccomp.
There is something called "linux capabilities" to make granular permissions for executing "privileged actions".

The `getcap` command displays the capabilities assigned to a binary. You can use it to inspect which specific privileges a process or executable has been granted, such as the ability to bind to low-numbered ports or send raw packets.

```bash
getcap /usr/bin/ping
ps -ef | grep sshd

getcap <process-id-of-sshd>
```
