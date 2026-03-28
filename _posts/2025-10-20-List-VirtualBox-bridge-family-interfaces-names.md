---
title: "List VirtualBox bridge family interfaces names"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=420&fit=crop"
description: "How to list all available bridged network interfaces in VirtualBox using the VBoxManage CLI tool."

tags: ['ml', 'virtualbox', 'bridge']
categories: ["Machine Learning"]
---

##  List VirtualBox bridge family interface names

Use the `VBoxManage` CLI to list all bridged network interfaces available on your host system. This is useful when configuring VirtualBox VMs to use bridged networking and you need to know the exact interface name to specify.

```bash
VBoxManage list bridgedifs
```
