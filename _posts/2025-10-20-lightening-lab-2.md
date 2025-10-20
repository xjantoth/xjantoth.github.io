---
title: "Lightening lab 2"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Lightening lab 2"

tags: ['lightening', 'lab']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

**Commands'':

```
controlplane $ for i in $(ls *.yaml); do echo filename: $i;echo "---" ;cat $i; done
```

```yaml

filename: 2.yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx1401
  namespace: dev1401
spec:
  containers:
  - image: kodekloud/nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    ports:
    - containerPort: 9080
      protocol: TCP
    livenessProbe:
      exec:
        command:
        - ls
        - /var/www/html/file_check
      initialDelaySeconds: 10
      periodSeconds: 60
    readinessProbe:
      failureThreshold: 3
      httpGet:
        path: /
        port: 9080
        scheme: HTTP
      periodSeconds: 10
      successThreshold: 1
      timeoutSeconds: 1
    resources: {}
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: default-token-xfbcr
      readOnly: true
  nodeName: node01
  volumes:
  - name: default-token-xfbcr
    secret:
      defaultMode: 420
      secretName: default-token-xfbcr
filename: 3.yaml
---
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  creationTimestamp: null
  name: dice
spec:
  jobTemplate:
    metadata:
      creationTimestamp: null
      name: dice
    spec:
      completions: 1
      backoffLimit: 25
      activeDeadlineSeconds: 20

      template:
        metadata:
          creationTimestamp: null
        spec:
          containers:
          - image: kodekloud/throw-dice
            name: throw-dice-pod
            resources: {}
          restartPolicy: Never
  schedule: '*/1 * * * *'
status: {}

filename: 4.yaml
---
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: my-busybox
  name: my-busybox
  namespace: dev2406
spec:
  volumes:
  - name: secret-volume
    secret:
      secretName: dotfile-secret
  nodeName: controlplane
  containers:
  - image: busybox
    name: secret
    resources: {}
    volumeMounts:
    - name: secret-volume
      mountPath: "/etc/secret-volume"
    command: ["sh", "-c", "sleep 3600"]
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
filename: 5.yaml
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-vh-routing
spec:
  rules:
  - host: "watch.ecom-store.com"
    http:
      paths:
      - pathType: Prefix
        path: "/video"
        backend:
          service:
            name: video-service
            port:
              number: 8080
  - host: "apparels.ecom-store.com"
    http:
      paths:
      - pathType: Prefix
        path: "/wear"
        backend:
          service:
            name: apparels-service
            port:
              number: 8080


filename: throw-a-dice.yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: throw-dice-pod
spec:
  containers:
  -  image: kodekloud/throw-dice
     name: throw-dice
  restartPolicy: Never
```


```
kubectl  get pod -n dev1401       nginx1401  -o yaml > 2.yaml
vim 2.yaml
kubectl  delete pod -n dev1401       nginx1401
kubectl  create cronjob dice --help
kubectl  create cronjob dice --schedule="*/1 * * * *" -o yaml --dry-run=client
kubectl  create cronjob dice --image=nginx --schedule="*/1 * * * *" -o yaml --dry-run=client
kubectl  create cronjob dice --image=nginx --schedule="*/1 * * * *" -o yaml --dry-run=client > 3.yaml
vim 3.yaml
kubectl create -f  3.yaml
kubectl create -f  2.yaml
vim 3.yaml
kubectl create -f  3.yaml
kubectl  get pods
kubectl  get pods -A
kubectl  run my-busybox -n dev2406 --image=busybox -- sleep 3600 --dry-run=client -o yaml
kubectl  get pods -n dev2406
kubectl  delete pod my-busybox -n dev2406
kubectl  get pods -A
kubectl  run my-busybox -n dev2406 --image=busybox  --dry-run=client -o yaml
kubectl  run my-busybox -n dev2406 --image=busybox  --dry-run=client -o yaml > 4.yaml
vim 4.yaml
kubectl create  -f  4.yaml
vim 2.yaml
kubectl  delete pod my-busybox -n dev2406
kubectl  delete pod -n dev1401       nginx1401
vim 5.yaml
kubectl  create -f 5.yaml
kubectl  create -f 2.yaml
kubectl  describe ing ingress-vh-routing
curl http://watch.ecom-store.com:30093/video
curl http://watch.ecom-store.com:30093/video -IL
http://apparels.ecom-store.com:30093/wear
curl http://apparels.ecom-store.com:30093/wear
curl http://apparels.ecom-store.com:30093/wear -IL
curl http://apparels.ecom-store.com:30093/weasasar -IL
kubectl get pods -A
kubectl  logs -f dev-pod-dind-878516
kubectl  logs -f dev-pod-dind-878516 -c log-x
kubectl  logs -f dev-pod-dind-878516 -c log-x > /opt/dind-878516_logs.txt
kubectl  logs  dev-pod-dind-878516 -c log-x > /opt/dind-878516_logs.txt
kubectl  get pod -n dev2406
vim 4.yaml
kubectl  create -f 4.yaml
kubectl delete pod secret -n dev2406
vim 4.yaml
kubectl  create -f 4.yaml
kubectl get pods -n dev2406
for i in $(ls *.yaml); do echo filename: $i;echo "---" ;cat $i; done

```
