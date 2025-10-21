---
title: "Drone CICD on Rancher Desktop MAC Kubernetes"
date: 2022-10-25T22:25:36+0200
lastmod: 2022-10-25T22:25:36+0200
draft: false
description: "Drone CICD on Rancher Desktop MAC Kubernetes"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['drone', 'cicd', 'rancher', 'desktop', 'mac', 'kubernetes']
---


# Drone CICD at Rancher on Desktop at Mac

### Setup `/etc/hosts` file


```
vim /etc/hosts

...
127.0.0.1       gitea-http drone

...
:wq!

```

Do not forget to setup `Port Forwarding` in Rancher Desktop App


Deploy Gitea and Drone with Kubernetes runner

```
helm upgrade --install drone drone/drone \
--set env.DRONE_GITEA_SERVER=http://gitea-http:30111 \
--set env.DRONE_GITEA_CLIENT_ID=53eb6510-6108-4138-b82a-fac48445b909 \
--set env.DRONE_GITEA_CLIENT_SECRET=gto_4afpn24sess36frowgtgvlydvu5wikho6fqvn7z2fnnjxfge4yfq \
--set env.DRONE_RPC_SECRET=admin-secret \
--set env.DRONE_SERVER_HOST=drone:30222 \
--set env.DRONE_SERVER_PROTO=http \
--set env.DRONE_USER_CREATE="username:misko\,admin:true" \
--set service.port=30222 \
--set env.DRONE_LOGS_DEBUG=true


helm upgrade --install gitea gitea-charts/gitea \
--set gitea.config.server.HTTP_PORT=30111 \
--set service.http.port=30111 \
--set gitea.config.server.ROOT_URL="http://gitea-http:30111"
--set gitea.config.webhook.ALLOWED_HOST_LIST="drone"

```

### Kubernetes runner

```yaml

kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: default
  name: drone
rules:
- apiGroups:
  - ""
  resources:
  - secrets
  verbs:
  - create
  - delete
- apiGroups:
  - ""
  resources:
  - pods
  - pods/log
  verbs:
  - get
  - create
  - delete
  - list
  - watch
  - update

---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: drone
  namespace: default
subjects:
- kind: ServiceAccount
  name: default
  namespace: default
roleRef:
  kind: Role
  name: drone
  apiGroup: rbac.authorization.k8s.io

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: drone-runner
  labels:
    app.kubernetes.io/name: drone
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: drone
  template:
    metadata:
      labels:
        app.kubernetes.io/name: drone
    spec:
      containers:
      - name: runner
        image: drone/drone-runner-kube:latest
        ports:
        - containerPort: 3000
        env:
        - name: DRONE_RPC_HOST
          value: drone:30222
        - name: DRONE_RPC_PROTO
          value: http
        - name: DRONE_RPC_SECRET
          value: admin-secret
```
