---
title: "Kubernetes SSL certificates"
date: 2022-01-13T15:17:08+01:00
lastmod: 2022-01-13T15:17:16+01:00
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Check SSL certificate validity"

tags: ['kubernetes', 'ssl', 'certificates']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---


There are many SSL certificates used by different Kubenretes components.

```
ls /etc/kubernetes/pki/ -l
total 60
-rw-r--r-- 1 root root 1155 Jan 13 13:06 apiserver-etcd-client.crt
-rw------- 1 root root 1679 Jan 13 13:06 apiserver-etcd-client.key
-rw-r--r-- 1 root root 1164 Jan 13 13:06 apiserver-kubelet-client.crt
-rw------- 1 root root 1679 Jan 13 13:06 apiserver-kubelet-client.key
-rw-r--r-- 1 root root 1289 Jan 13 13:06 apiserver.crt
-rw------- 1 root root 1679 Jan 13 13:06 apiserver.key
-rw-r--r-- 1 root root 1099 Jan 13 13:06 ca.crt
-rw------- 1 root root 1675 Jan 13 13:06 ca.key
drwxr-xr-x 2 root root 4096 Jan 13 13:06 etcd
-rw-r--r-- 1 root root 1115 Jan 13 13:06 front-proxy-ca.crt
-rw------- 1 root root 1679 Jan 13 13:06 front-proxy-ca.key
-rw-r--r-- 1 root root 1119 Jan 13 13:06 front-proxy-client.crt
-rw------- 1 root root 1679 Jan 13 13:06 front-proxy-client.key
-rw------- 1 root root 1679 Jan 13 13:06 sa.key
-rw------- 1 root root  451 Jan 13 13:06 sa.pub
```

Please notic this files within /etc/kubernetes folder

```
root@scw-k8s-cks:~# ls /etc/kubernetes/ -l
total 36
-rw------- 1 root root 5635 Jan 13 13:06 admin.conf
-rw------- 1 root root 5671 Jan 13 13:06 controller-manager.conf  <-- kubeconfig for controller manager
-rw------- 1 root root 1979 Jan 13 13:07 kubelet.conf             <-- kubeconfig for kubelet
drwxr-xr-x 2 root root 4096 Jan 13 13:06 manifests
drwxr-xr-x 3 root root 4096 Jan 13 13:06 pki
-rw------- 1 root root 5619 Jan 13 13:06 scheduler.conf           <-- kubeconfig for scheduler

```

**Check client/server kubelet certificates''

```
# Check client/server kubelet certificates

# server
openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet.crt

#client
openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet-client-current.pem
```

```go
# renew certificate
kubeadm certs renew  apiserver

# Check SSL cert validity
ssh cluster2-master1 kubeadm certs check-expiration --cert-dir  /etc/kubernetes/pki

[check-expiration] Reading configuration from the cluster...
[check-expiration] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'

CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE AUTHORITY   EXTERNALLY MANAGED
admin.conf                 Mar 18, 2022 12:04 UTC   364d                                    no
apiserver                  Mar 18, 2022 12:04 UTC   364d            ca                      no
apiserver-etcd-client      Mar 18, 2022 12:04 UTC   364d            etcd-ca                 no
apiserver-kubelet-client   Mar 18, 2022 12:04 UTC   364d            ca                      no
controller-manager.conf    Mar 18, 2022 12:04 UTC   364d                                    no
etcd-healthcheck-client    Mar 18, 2022 12:04 UTC   364d            etcd-ca                 no
etcd-peer                  Mar 18, 2022 12:04 UTC   364d            etcd-ca                 no
etcd-server                Mar 18, 2022 12:04 UTC   364d            etcd-ca                 no
front-proxy-client         Mar 18, 2022 12:04 UTC   364d            front-proxy-ca          no
scheduler.conf             Mar 18, 2022 12:04 UTC   364d                                    no

CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY MANAGED
ca                      Jan 20, 2031 19:41 UTC   9y              no
etcd-ca                 Jan 20, 2031 19:41 UTC   9y              no
front-proxy-ca          Jan 20, 2031 19:41 UTC   9y              no

---
sh cluster2-master1  openssl x509 -noout -text -in /etc/kubernetes/pki/apiserver.crt | grep -i Valid -A4 -B4
        Version: 3 (0x2)
        Serial Number: 1102934230143616014 (0xf4e68d6b654440e)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN = kubernetes
        Validity
            Not Before: Jan 22 19:41:03 2021 GMT
            Not After : Mar 18 12:04:23 2022 GMT
        Subject: CN = kube-apiserver
        Subject Public Key Info:
```
