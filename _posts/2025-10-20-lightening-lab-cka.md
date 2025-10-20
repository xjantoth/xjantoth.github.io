---
title: "Lightening Lab - CKA"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Lightening Lab - CKA"

tags: ['lightening', 'lab', 'cka']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

Some other notes

```
kubectl  get pvc
NAME          STATUS   VOLUME     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
alpha-claim   Bound    alpha-pv   1Gi        RWO            slow           4s
controlplane $ kubectl  get pods
NAME                           READY   STATUS              RESTARTS   AGE
alpha-mysql-74ffffd5df-k55wj   0/1     ContainerCreating   0          9s
controlplane $ watch kubectl  get pods
controlplane $
controlplane $
controlplane $
controlplane $
controlplane $
controlplane $ watch kubectl  get pods^C
controlplane $ cat 5.yaml
#apiVersion: v1
#kind: PersistentVolume
#metadata:
#  name: alpha-pv
#spec:
#  accessModes:
#  - ReadWriteOnce
#  capacity:
#    storage: 1Gi
#  hostPath:
#    path: /opt/pv-1
#    type: ""
#  persistentVolumeReclaimPolicy: Retain
#  storageClassName: slow
#  volumeMode: Filesystem

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: alpha-claim
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: slow
  volumeMode: Filesystem

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alpha-mysql
  namespace: alpha
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: alpha-mysql
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: alpha-mysql
    spec:
      containers:
      - env:
        - name: MYSQL_ALLOW_EMPTY_PASSWORD
          value: "1"
        image: mysql:5.6
        imagePullPolicy: Always
        name: mysql
        ports:
        - containerPort: 3306
          protocol: TCP
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /var/lib/mysql
          name: mysql-data
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
      volumes:
      - name: mysql-data
        persistentVolumeClaim:
          claimName: alpha-claim
```

```
# Update K8s controlplane
apt update
apt-cache madison kubeadm
apt-get update && apt-get install -y kubeadm=1.19.0-00
kubeadm version
kubectl  get nodes
kubeadm upgrade apply v1.19.0
kubectl drain controlplane --ignore-daemonsets
kubectl  get pods -A -owide
apt-get update && apt-get install -y kubelet=1.19.0-00 kubectl=1.19.0-00
systemctl daemon-reload
systemctl restart kubelet
kubectl  get nodes
kubectl  uncordon  controlplane
kubectl  get nodes
kubectl  drain node01 --ignore-daemonsets

ssh node01
apt-get update && apt-get install -y kubeadm=1.19.0-00
kubeadm version
kubeadm upgrade node
apt-get update && apt-get install -y kubelet=1.19.0-00 kubectl=1.19.0-00
...

kubectl  create  deployment  nginx-deploy --image=nginx:1.16
kubectl  rollout history deployment nginx-deploy
kubectl  set image deployment  nginx-deploy *=nginx:1.17 --record
kubectl  rollout history deployment nginx-deploy
kubectl  config set-context --current --namespace alpha

export ETCDCTL_API=3
etcdctl snapshot save /opt/etcd-backup.db    --cacert /etc/kubernetes/pki/etcd/ca.crt --key /etc/kubernetes/pki/etcd/server.key  --cert /etc/kubernetes/pki/etcd/server.crt
ls /opt/etcd-backup.db
kubectl   run secret-1401 -n admin1401 --image=busybox  -o yaml --dry-run=client > 7.yaml
vim 7.yaml
kubectl  exec -it -n admin1401  secret-1401 -- sh

kubectl  get deploy -n admin2406 -o custom-columns=DEPLOYMENT:.metadata.name,CONTAINER_IMAGE:.spec.template.spec.containers[*].image,READY_REPLICAS:.spec.replicas,NAMESPACE:.metadata.namespace --sort-by=.metadata.name > /opt/admin2406_data
```

```yaml
for i in $(ls *.yaml); do echo -e "$i\n\n"; cat $i; done
7.yaml


apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secret-1401
  name: secret-1401
  namespace: admin1401
spec:
  containers:
  - command:
    - sleep
    - "4800"
    image: busybox
    name: secret-admin
    resources: {}
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secret-volume
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: dotfile-secret
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
pvc.yaml


apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: alpha-claim
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  volumeMode: Filesystem
pv.yaml


apiVersion: v1
kind: PersistentVolume
metadata:
  name: alpha-pv
spec:
  accessModes:
  - ReadWriteMany
  capacity:
    storage: 1Gi
  hostPath:
    path: /opt/pv-1
  persistentVolumeReclaimPolicy: Retain
  volumeMode: Filesystem
```
