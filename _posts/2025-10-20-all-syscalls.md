---
title: "All syscalls"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Learn about Linux syscalls and seccomp profiles for Kubernetes, including how to look up syscall numbers and create audit and violation profiles."

tags: ['all', 'syscalls']
categories: ["DevOps"]
---

## Learn about syscalls and seccomp

Understanding Linux syscalls is essential for configuring seccomp profiles in Kubernetes. The commands below show how to look up specific syscall numbers and set up seccomp profiles in the default kubelet directory for use with pods.

```bash
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
