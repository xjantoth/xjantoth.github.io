---
title: "PodSecurityPolicy"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "PodSecurityPolicy"

tags: ['podsecuritypolicy']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

**Setup API server to allow PodSecurityPolicy Admission controller''

```yaml
cat /etc/kubernetes/manifests/kube-apiserver.yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    kubeadm.kubernetes.io/kube-apiserver.advertise-address.endpoint: 10.156.0.2:6443
  creationTimestamp: null
  labels:
    component: kube-apiserver
    tier: control-plane
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --advertise-address=10.156.0.2
    - --allow-privileged=true
    - --encryption-provider-config=/etc/kubernetes/etcd/ec.yaml
    - --anonymous-auth=true
    - --authorization-mode=Node,RBAC
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --enable-admission-plugins=NodeRestriction,PodSecurityPolicy
    - --enable-bootstrap-token-auth=true
...
```
**Create podsecuritypolicy in cluster''

```yaml
cat psp.yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: default
spec:
  allowedCapabilities:
  - NET_ADMIN
  allowPrivilegeEscalation: false
  privileged: false  # Don't allow privileged pods!
  # The rest fills in some required fields.
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  runAsUser:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
  volumes:
  - '*'
```
**Create corresponding role/rolebinding for default serviceaccunt to be able to use PodSecurityPolicy''

```perl
k create  role psp-access --verb=use --resource=podsecuritypolicies
k create  rolebinding  psp-access --role psp-access --serviceaccount default:default
k create  deployment  nginx --image=nginx
```


**Create proxy pod for mTLS''

```yaml
cat proxy.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: proxy
  name: proxy
spec:
  containers:
  - command:
    - ping
    - google.com
    image: bash
    name: base
    resources: {}
  - name: proxy
    image: ubuntu
    command:
    - sh
    - -c
    - 'apt-get update  && apt-get install iptables -y && iptables -L && sleep 1d'
    securityContext:
      capabilities:
        add: ["NET_ADMIN"]
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}


```
