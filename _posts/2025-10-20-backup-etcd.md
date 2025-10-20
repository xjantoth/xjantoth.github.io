---
title: "Backup ETCD"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Backup ETCD"

tags: ['backup', 'etcd']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
export ETCDCTL_API=3
etcdctl  snapshot save  /opt/snapshot-pre-boot.db  --cert=/etc/kubernetes/pki/etcd/server.crt  --cacert=/etc/kubernetes/pki/etcd/ca.crt --key=/etc/kubernetes/pki/etcd/server.key
```
