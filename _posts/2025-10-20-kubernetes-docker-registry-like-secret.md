---
title: "Kubernetes docker-registry like secret"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Create a Kubernetes docker-registry secret and configure a deployment to use imagePullSecrets for private container registries."

tags: ['kubernetes', 'like', 'secret']
categories: ["Kubernetes"]
---

**Create a Secret by providing credentials on the command line**

Use `kubectl create secret docker-registry` to store your private registry credentials as a Kubernetes secret. This secret can then be referenced by pods to pull images from authenticated registries.

```bash
k create  secret docker-registry \
private-reg-cred --docker-server=myprivateregistry.com:5000 \
--docker-username=dock_user \
--docker-password=dock_password \
--docker-email=dock_user@myprivateregistry.com

secret/private-reg-cred created
```

**Edit your custom deployment and add imagePullSecrets under the container spec**

After creating the secret, edit the deployment to reference it. The `imagePullSecrets` field tells Kubernetes which credentials to use when pulling the container image.

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
