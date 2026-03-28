---
title: "Backup ETCD"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to create an etcd snapshot backup using etcdctl with TLS certificates on a Kubernetes cluster."

tags: ['etcd']
categories: ["DevOps"]
---

To create a backup of the etcd datastore, use `etcdctl snapshot save`. You must specify the TLS certificates used by the etcd server, which are typically located under `/etc/kubernetes/pki/etcd/` on kubeadm-based clusters. Set the `ETCDCTL_API` environment variable to `3` to use the v3 API.

```bash
export ETCDCTL_API=3
etcdctl  snapshot save  /opt/snapshot-pre-boot.db  --cert=/etc/kubernetes/pki/etcd/server.crt  --cacert=/etc/kubernetes/pki/etcd/ca.crt --key=/etc/kubernetes/pki/etcd/server.key
```
