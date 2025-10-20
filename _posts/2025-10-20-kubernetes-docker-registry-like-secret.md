---
title: "Kubernetes docker-registry like secret"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Kubernetes docker-registry like secret"

tags: ['kubernetes', 'like', 'secret']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

**Create a Secret by providing credentials on the command line''

```
k create  secret docker-registry \
private-reg-cred --docker-server=myprivateregistry.com:5000 \
--docker-username=dock_user \
--docker-password=dock_password \
--docker-email=dock_user@myprivateregistry.com

secret/private-reg-cred created
```

**Edit your custom deployment and provide: imagePullSecrets under container spec''

```yaml
kubectl edit deployment web
...
    spec:
      containers:
      - image: myprivateregistry.com:5000/nginx:alpine
        imagePullPolicy: IfNotPresent
        name: nginx
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      imagePullSecrets:
      - name: private-reg-cred

```
