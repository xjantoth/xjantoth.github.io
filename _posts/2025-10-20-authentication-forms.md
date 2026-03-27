---
title: "Authentication forms"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "**Authentication'' against KUBE-API server."

tags: ['authentication', 'forms']
categories: ["DevOps"]
---

**Authentication'' against KUBE-API server

1. `--basic-auth-file=/path/to/some.csv`  and use this flag for ''kubeapi-server'' configuration (not recommended)<br>
2.  `--token-auth-file=/path/to/some.csv`  and use this flag for ''kubeapi-server'' configuration (not recommended)<br>

3. certificate

```
cat  csr.yaml
apiVersion: certificates.k8s.io/v1beta1
kind: CertificateSigningRequest
metadata:
  name: akshay
spec:
  groups:
  - system:authenticated
  request: |         LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFQYnlDNEZ4QS9zbWFQQ2crSUlOZXJYdGY2TDQ9Ci0t
         LS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
  signerName: kubernetes.io/kube-apiserver-client-kubelet
  usages:
  - digital signature
  - key encipherment
  - client auth
```
