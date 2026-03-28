---
title: "Game of Pods - App Gallery"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "KodeKloud Game of Pods App Gallery challenge: deploy an Iron Gallery app with MariaDB, Ingress, and a NetworkPolicy."

tags: ['game', 'pods', 'app', 'gallery']
categories: ["Kubernetes"]
---

This solution to the "Game of Pods - App Gallery" challenge deploys an Iron Gallery application backed by a MariaDB database, with an Ingress for external access and a NetworkPolicy restricting database traffic to only the gallery pods on port 3306.

```yaml
for i in $(ls *.yaml); do echo filename: $i;echo "---" ;cat $i; done
filename: ingress.yaml
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: iron-gallery-ingress
spec:
  rules:
  - host: "iron-gallery-braavos.com"
    http:
      paths:
      - path: /
        backend:
          serviceName: iron-gallery-service
          servicePort: 80

filename: iron-db.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: iron-db
  name: iron-db
spec:
  replicas: 1
  selector:
    matchLabels:
      app: iron-db
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: iron-db
        db: mariadb
    spec:
      volumes:
      - name: db
        emptyDir: {}
      containers:
      - image: kodekloud/irondb:2.0
        name: irondb
        resources: {}
        volumeMounts:
        - name: db
          mountPath: '/var/lib/mysql'
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "Braavo"
        - name: MYSQL_DATABASE
          value: "lychee"
        - name: MYSQL_USER
          value: "lychee"
        - name: MYSQL_PASSWORD
          value: "lychee"

status: {}
filename: iron-gallery.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: iron-gallery
  name: iron-gallery
spec:
  replicas: 1
  selector:
    matchLabels:
      app: iron-gallery
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: iron-gallery
        run: iron-gallery
    spec:
      volumes:
      - name: config
        emptyDir: {}
      - name: images
        emptyDir: {}
      containers:
      - image: kodekloud/irongallery:2.0
        name: irongallery
        resources: {}
        volumeMounts:
        - name: config
          mountPath: '/usr/share/nginx/html/data'
        - name: images
          mountPath: '/usr/share/nginx/html/uploads'
status: {}
filename: netpol.yaml
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: iron-gallery-firewall
  namespace: default
spec:
  podSelector:
    matchLabels:
      db: mariadb
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          run: iron-gallery
    ports:
    - protocol: TCP
      port: 3306
```
