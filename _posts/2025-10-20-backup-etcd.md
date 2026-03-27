---
title: "Backup ETCD"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Backup ETCD — practical walkthrough with examples."

tags: ['etcd']
categories: ["DevOps"]
---

```
export ETCDCTL_API=3
etcdctl  snapshot save  /opt/snapshot-pre-boot.db  --cert=/etc/kubernetes/pki/etcd/server.crt  --cacert=/etc/kubernetes/pki/etcd/ca.crt --key=/etc/kubernetes/pki/etcd/server.key
```
