---
title: "Lightening lab 1"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Lightening lab 1"

tags: ['lightening', 'lab']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: nginx-deploy
  name: nginx-deploy
spec:
  replicas: 4
  selector:
    matchLabels:
      app: nginx-deploy
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: nginx-deploy
    spec:
      containers:
      - image: nginx:1.16
        name: nginx
        resources: {}
status: {}

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: x-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: secure-pod
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: webapp-color
    ports:
    - protocol: TCP
      port: 80

---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: log-volume
spec:
  capacity:
    storage: 1Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteMany
  storageClassName: "manual"
  hostPath:
    path: "/opt/volume/nginx"


---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: log-claim
spec:
  storageClassName: "manual"
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 200Mi

---
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: logger
  name: logger
spec:
  volumes:
  - name: vol
    persistentVolumeClaim:
      claimName: log-claim
  containers:
  - image: nginx:alpine
    name: logger
    resources: {}
    volumeMounts:
    - name: vol
      mountPath: "/var/www/nginx"
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

---
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: redis
  name: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: redis
    spec:
      nodeName: controlplane
      volumes:
      - name: data
        emptyDir: {}
      - name: redis-config
        configMap:
          name: redis-config
      containers:
      - image: redis:alpine
        name: redis
        ports:
        - containerPort: 6397
        volumeMounts:
        - name: data
          mountPath: "/redis-master-data"
        - name: redis-config
          mountPath: "/redis-master"
        resources:
          requests:
            cpu: 0.2

status: {}

---
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: time-check
  name: time-check
  namespace: dvl1987
spec:

  volumes:
  - name: temp
    emptyDir: {}
  containers:
  - image: busybox
    name: time-check
    command: ["sh", "-c", "while true; do date; sleep $TIME_FREQ;done > /opt/time/time-check.log"]
    env:
      # Define the environment variable
      - name: TIME_FREQ  # Notice that the case is different here
                                   # from the key name in the ConfigMap.
        valueFrom:
          configMapKeyRef:
            name: time-config           # The ConfigMap this value comes from.
            key: TIME_FREQ
    volumeMounts:
    - name: temp
      mountPath: "/opt/time"
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
controlplane $
controlplane $
```
