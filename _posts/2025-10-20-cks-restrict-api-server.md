---
title: "CKS Restrict API server"
date: 2022-04-05T14:14:34+0200
lastmod: 2022-04-05T14:14:34+0200
draft: false
description: "Restricting access to the Kubernetes API server using anonymous auth, insecure port, and the NodeRestriction admission plugin."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['cks', 'api', 'server']
categories: ["Kubernetes"]
---

#### There is a flag when starting `kube-apiserver` called:

The `--anonymous-auth` flag controls whether anonymous requests to the API server are allowed. When set to `true`, unauthenticated requests are assigned the `system:anonymous` username and the `system:unauthenticated` group.

```bash
kube-apiserver --anonymous-auth=true|false
```

The default value for this option is `true` because some liveness and readiness probes need it.

#### Then we have --insecure-port=8080 (deprecated)

There was an option in the past before Kubernetes 1.20 to use the `--insecure-port` flag. In such a case, all authentication and authorization to the API server would be skipped, and this was and still is considered highly insecure and dangerous.

```bash
kube-apiserver --insecure-port=8080
```


#### Call API server via curl

To make direct API calls to the Kubernetes API server using `curl`, you first need to extract the certificate authority, client certificate, and client key from your kubeconfig. These are then passed to `curl` for mutual TLS authentication.

```bash
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

```yaml
    - kube-apiserver
    ...
    - --enable-admission-plugins=NodeRestriction
    ...
```

Here are several examples of what can and cannot be done by using this KUBECONFIG file. The kubelet is able to list pods and nodes but cannot list namespaces because the NodeRestriction plugin limits the kubelet's permissions.

```bash
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

We are not allowed to modify special labels like `node-restriction.kubernetes.io/*` when the NodeRestriction admission plugin is enabled.

```bash
root@lima-k8s:~# kubectl label node lima-k8s node-restriction.kubernetes.io/test=yes
Error from server (Forbidden): nodes "lima-k8s" is forbidden: is not allowed to modify labels: node-restriction.kubernetes.io/test```


#### Troubleshooting

If the kube-apiserver fails to start after a configuration change, use `crictl` to inspect the container state and view its logs. The container will appear in an `Exited` state with error messages indicating the problem.

```bash
crictl ps -a
CONTAINER           IMAGE               CREATED             STATE               NAME                      ATTEMPT             POD ID
9b69ae66f21ad       b6d7abedde399       25 seconds ago      Exited              kube-apiserver            4                   0bbfc476e406a
...
controlplane $ crictl logs -f 9b69ae66f21ad
Error: unknown flag: --this-is-very-wrong
```


###### Log locations to check:

When troubleshooting kube-apiserver issues, the following log locations and commands are the most useful for diagnosing startup failures or misconfigurations.

```bash
/var/log/pods
/var/log/containers
crictl ps + crictl logs
docker ps + docker logs (in case when Docker is used)
kubelet logs: /var/log/syslog or journalctl
```

###### NodeRestriction in kube-apiserver manifest

We need to enable the NodeRestriction in the API server manifest. Add the `--enable-admission-plugins=NodeRestriction` flag to the kube-apiserver command arguments in the static pod manifest.

```yaml
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
