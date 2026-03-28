---
title: "PodSecurityPolicy"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "How to enable the PodSecurityPolicy admission controller in the Kubernetes API server, create a policy, and bind it to a service account."

tags: ['podsecuritypolicy']
categories: ["Kubernetes"]
---

## Setup API server to allow PodSecurityPolicy Admission controller

To enable PodSecurityPolicy, you need to add it to the `--enable-admission-plugins` flag in the kube-apiserver static pod manifest. After saving the file, the kubelet will automatically restart the API server.

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
## Create PodSecurityPolicy in the cluster

This policy allows `NET_ADMIN` capability but disallows privilege escalation and privileged containers. It uses permissive rules for SELinux, supplemental groups, run-as-user, and fsGroup.

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
## Create corresponding role/rolebinding for the default service account to use the PodSecurityPolicy

After creating the policy, you must grant the service account permission to "use" it via a Role and RoleBinding. Without this, pod creation will be denied by the admission controller.

```bash
k create  role psp-access --verb=use --resource=podsecuritypolicies
k create  rolebinding  psp-access --role psp-access --serviceaccount default:default
k create  deployment  nginx --image=nginx
```


## Create proxy pod for mTLS

This pod runs two containers: one that pings google.com and a proxy container that installs iptables and lists the current rules. The proxy container requires the `NET_ADMIN` capability, which is allowed by the PodSecurityPolicy created above.

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
