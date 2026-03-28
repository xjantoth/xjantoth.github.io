---
title: "Drone CICD on Rancher Desktop MAC Kubernetes"
date: 2022-10-25T22:25:36+0200
lastmod: 2022-10-25T22:25:36+0200
draft: false
description: "How to set up Drone CI/CD with Gitea on Rancher Desktop for Mac, including Helm deployments and a Kubernetes runner."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['drone', 'cicd', 'rancher', 'desktop', 'mac', 'kubernetes']
categories: ["Kubernetes"]
---


# Drone CI/CD on Rancher Desktop for Mac

### Setup `/etc/hosts` file

Add local DNS entries for Gitea and Drone so that services can resolve each other by hostname on your local machine.

```bash
vim /etc/hosts

...
127.0.0.1       gitea-http drone

...
:wq!

```

Do not forget to setup `Port Forwarding` in Rancher Desktop App


Deploy Gitea and Drone using Helm. The Drone chart is configured to use Gitea as the SCM provider via OAuth credentials, and Gitea is set up with a custom HTTP port and webhook allowlist.

```bash
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

The following manifests create the RBAC Role and RoleBinding needed by the Drone Kubernetes runner, plus a Deployment that runs the runner container itself. The runner connects to the Drone server via RPC to pick up and execute pipeline steps as Kubernetes pods.

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
