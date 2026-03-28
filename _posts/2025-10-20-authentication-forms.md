---
title: "Authentication forms"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Overview of authentication methods against the Kubernetes API server, including basic auth, token auth, and certificate-based authentication."

tags: ['authentication', 'forms']
categories: ["DevOps"]
---

## Authentication against the Kubernetes API server

There are several ways to authenticate against the Kubernetes API server. The first two methods are deprecated and not recommended for production use.

1. `--basic-auth-file=/path/to/some.csv` and use this flag for kube-apiserver configuration (not recommended)
2. `--token-auth-file=/path/to/some.csv` and use this flag for kube-apiserver configuration (not recommended)

3. Certificate-based authentication (recommended)

The following YAML defines a CertificateSigningRequest resource, which is the preferred way to request client certificates for user authentication in Kubernetes.

```yaml
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
