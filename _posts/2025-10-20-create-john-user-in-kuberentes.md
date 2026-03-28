---
title: "Create John user in Kubernetes"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Creating a Kubernetes user with certificate-based authentication, including CSR approval, RBAC role and rolebinding setup, and kubeconfig configuration."

tags: ['john', 'user', 'kuberentes']
categories: ["Kubernetes"]
---

The following steps create a user called "john" in Kubernetes using certificate-based authentication. This involves creating an RBAC role and rolebinding, submitting a CertificateSigningRequest, approving it, extracting the signed certificate, and configuring a kubeconfig context.

```bash
kubectl  create  role developer --verb=create,list,get,update,delete --resource pods --namespace development
kubectl  create  rolebinding john-role-binding --role developer --user john --namespace development

apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: john
spec:
  groups:
  - system:authenticated
  request: LS0t...
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth

:r! cat /root/CKA/john.csr | base64 | tr -d "\n"

kubectl  get csr
kubectl  certificate approve john

kubectl get csr/john -o yaml
kubectl get csr/john -o yaml -ojsonpath='{.status.certificate}'
kubectl get csr/john -o yaml -ojsonpath='{.status.certificate}' | base64 -d
kubectl get csr/john -o yaml -ojsonpath='{.status.certificate}' | base64 -d > CKA/john.crt
kubectl config set-credentials john --client-key=/root/CKA/john.key --client-certificate=/root/CKA/john.crt --embed-certs=true
kubectl config set-context john --cluster=kubernetes --user=john
kubectl config use-context john
kubectl  get pods -n development
```
