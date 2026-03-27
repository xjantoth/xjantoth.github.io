---
title: "All syscalls"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "**Learn about syscalls and seccomp''."

tags: ['all', 'syscalls']
categories: ["DevOps"]
---

**Learn about syscalls and seccomp''

```
# Each and every syscall explained
grep -w 35 /usr/include/asm/unistd_64.h
#define __NR_nanosleep 35


# Create seccomp profiles in a "default" location
sudo mkdir -p /var/lib/kubelet/seccomp/profiles
sudo touch  /var/lib/kubelet/seccomp/profiles/audit.json
sudo touch  /var/lib/kubelet/seccomp/profiles/violation.json

# Allow logging
sudo cat   /var/lib/kubelet/seccomp/profiles/audit.json
{
    "defaultAction": "SCMP_ACT_LOG"
}

# Disable use of any syscall by default

sudo cat   /var/lib/kubelet/seccomp/profiles/violation.json
{
    "defaultAction": "SCMP_ACT_ERRNO"
}


```
