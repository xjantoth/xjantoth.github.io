---
title: "Game of Pods - Redis cluster"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Game of Pods - Redis cluster"

tags: ['game', 'of', 'pods', 'redis', 'cluster']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
for i in {1..6}; do ssh node01 mkdir /redis0${i}; done
ssh node01 ls /redis*
```

```yaml
for i in $(ls *.yaml); do echo filename: $i;echo "---" ;cat $i; done
filename: pv.yaml
---
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis01
spec:
  capacity:
    storage: 1Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  hostPath:
    path: /redis01

---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis02
spec:
  capacity:
    storage: 1Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  hostPath:
    path: /redis02
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis03
spec:
  capacity:
    storage: 1Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  hostPath:
    path: /redis03
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis04
spec:
  capacity:
    storage: 1Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  hostPath:
    path: /redis04
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis05
spec:
  capacity:
    storage: 1Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  hostPath:
    path: /redis05
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis06
spec:
  capacity:
    storage: 1Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  hostPath:
    path: /redis06
filename: ss.yaml
---
apiVersion: v1
kind: Service
metadata:
  name: redis-cluster-service
  labels:
    app: redis-cluster
spec:
  ports:
  - port: 6379
    name: client
    targetPort: 6379
  - port: 16379
    name: gossip
    targetPort: 16379
  clusterIP: None
  selector:
    app: redis-cluster
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-cluster
spec:
  selector:
    matchLabels:
      app: redis-cluster # has to match .spec.template.metadata.labels
  serviceName: "redis-cluster-service"
  replicas: 6 # by default is 1
  template:
    metadata:
      labels:
        app: redis-cluster # has to match .spec.selector.matchLabels
    spec:
      terminationGracePeriodSeconds: 10
      volumes:
      - name: conf
        configMap:
          name: redis-cluster-configmap
          defaultMode: 0755
      - name: data
        persistentVolumeClaim:
          claimName: data
      containers:
      - name: redis
        env:
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        command: ["/conf/update-node.sh", "redis-server", "/conf/redis.conf"]
        image: redis:5.0.1-alpine
        ports:
        - containerPort: 6379
          name: client
        - containerPort: 16379
          name: gossip
        volumeMounts:
        - name: data
          mountPath: /data
          readOnly: false
        - name: conf
          mountPath: /conf
          readOnly: false
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```
