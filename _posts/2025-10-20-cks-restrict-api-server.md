---
title: "CKS Restrict API server"
date: 2022-04-05T14:14:34+0200
lastmod: 2022-04-05T14:14:34+0200
draft: false
description: "CKS Restrict API server"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['cks', 'restrict', 'api', 'server']
---

#### There is an flag when starting `kube-aoiserver` called:


```
kube-apiserver --anonymous-auth=true|false
```

The default value for this option is `true` because some liveness and readiness probes needs it.

#### Then we have --insecure-port=8080 (deprecated)

There was an option in past before Kubernetes 1.20 to use
In such a case, all authentication and authorization to API server would be skipped and this was and still is considered as highly insecure and dangerous.

```
kube-apiserver --insecure-port=8080
```


#### Call API server via curl


```
# Certification authority
k config view -o jsonpath='{.clusters[].cluster.certificate-authority-data}' --raw | base64 -d > ca

# Client certificate
k config view -o jsonpath='{.users[].user.client-certificate-data}' --raw  | base64 -d > crt

# Client key
k config view -o jsonpath='{.users[].user.client-key-data}' --raw | base64 -d > key

curl https://127.0.0.1:6443 --cacert ca --cert crt --key key
{
  "paths": [
    "/.well-known/openid-configuration",
    "/api",
    "/api/v1",
    "/apis",
    "/apis/",
    "/apis/admissionregistration.k8s.io",
    "/apis/admissionregistration.k8s.io/v1",
    "/apis/apiextensions.k8s.io",
    "/apis/apiextensions.k8s.io/v1",
    "/apis/apiregistration.k8s.io",
    "/apis/apiregistration.k8s.io/v1",
    "/apis/apps",
    "/apis/apps/v1",
    "/apis/authentication.k8s.io",
    "/apis/authentication.k8s.io/v1",
    "/apis/authorization.k8s.io",
    "/apis/authorization.k8s.io/v1",
    "/apis/autoscaling",
    "/apis/autoscaling/v1",
    "/apis/autoscaling/v2"
    ...
}
```


#### NodeRestriction plugin

Kubernetes **nodes** do have their own `kubeconfig` file located at `/etc/kubernetes/kubelet.conf` to communicate to **kube-apiserver** however, their permissions are limited.

```
    - kube-apiserver
    ...
    - --enable-admission-plugins=NodeRestriction
    ...
```

Here are several examples what can/cannot be done by using this KUBECONFIG file

```
root@lima-k8s:~# kubectl get pods --kubeconfig /etc/kubernetes/kubelet.conf
NAME             READY   STATUS    RESTARTS   AGE
accessor         1/1     Running   0          26h
krissko          1/1     Running   0          6d1h
pod-in-default   1/1     Running   0          6d1h
root@lima-k8s:~# kubectl get nodes --kubeconfig /etc/kubernetes/kubelet.conf
NAME       STATUS   ROLES                  AGE    VERSION
lima-k8s   Ready    control-plane,master   6d1h   v1.23.4
root@lima-k8s:~# kubectl get ns --kubeconfig /etc/kubernetes/kubelet.conf
Error from server (Forbidden): namespaces is forbidden: User "system:node:lima-k8s" cannot list resource "namespaces" in API group "" at the cluster scope
```

We are not allowed to modify special labels like

```
root@lima-k8s:~# kubectl label node lima-k8s node-restriction.kubernetes.io/test=yes
Error from server (Forbidden): nodes "lima-k8s" is forbidden: is not allowed to modify labels: node-restriction.kubernetes.io/test```


#### Troubleshooting


```
crictl ps -a
CONTAINER           IMAGE               CREATED             STATE               NAME                      ATTEMPT             POD ID
9b69ae66f21ad       b6d7abedde399       25 seconds ago      Exited              kube-apiserver            4                   0bbfc476e406a
...
controlplane $ crictl logs -f 9b69ae66f21ad
Error: unknown flag: --this-is-very-wrong
```


###### Log locations to check:

```
/var/log/pods
/var/log/containers
crictl ps + crictl logs
docker ps + docker logs (in case when Docker is used)
kubelet logs: /var/log/syslog or journalctl
```

###### NodeRestriction in kube-apiserver manifest

We need to enable the NodeRestriction in the Apiserver manifest

```
spec:
  containers:
  - command:
    - kube-apiserver
    - --advertise-address=172.30.1.2
    - --allow-privileged=true
    - --authorization-mode=Node,RBAC
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --enable-admission-plugins=NodeRestriction
    - --enable-bootstrap-token-auth=true
