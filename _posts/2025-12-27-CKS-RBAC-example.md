---
title: "CKS RBAC example"
date: 2025-12-27T20:25:14:+0100
lastmod: 2025-12-27T20:25:14:+0100
draft: false
description: "CKS exam topic: RBAC example showing ClusterRole, ClusterRoleBinding, Role, and RoleBinding for certificate signing request approval."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ["cks", "rbac", "csr"]
categories: ["Kubernetes"]
---

This example demonstrates a Kubernetes RBAC setup for the CKS exam. It creates a ClusterRole with permissions to approve CertificateSigningRequests, a ClusterRoleBinding to associate it with a ServiceAccount, and a namespace-scoped Role and RoleBinding for reading ConfigMaps.

```bash
cat cr.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: approver
rules:
- apiGroups:
  - certificates.k8s.io
  resources:
  - certificatesigningrequests
  verbs:
  - get
  - list
- apiGroups:
  - certificates.k8s.io
  resources:
  - certificatesigningrequests/approval
  verbs:
  - update
- apiGroups:
  - certificates.k8s.io
  resources:
  - signers
  resourceNames:
  - kubernetes.io.com/kube-apiserver-client # example.com/* can be used to authorize for all signers in the 'example.com' domain
  verbs:
  - approve
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: approver
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: approver
subjects:
- kind: ServiceAccount
  name: cert-signer
  namespace: team-lilac


....
cat rrb.yaml 
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: reader
  namespace: team-lilac
rules:
- apiGroups:
  - ""
  resources:
  - configmaps
  verbs:
  - list
  - get
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: reader
  namespace: team-lilac
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: reader
subjects:
- kind: ServiceAccount
  name: cert-signer
  namespace: team-lilac

```

