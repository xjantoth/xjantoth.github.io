---
title: "kubectl commands"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "kubectl commands"

tags: ['kubectl', 'commands']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

##  kubectl sort by

```python
kubectl get pods -A --sort-by=.metadata.name
NAMESPACE     NAME                                      READY   STATUS      RESTARTS   AGE
kube-system   coredns-854c77959c-m972h                  1/1     Running     0          5h38m
kube-system   helm-install-traefik-hx29s                0/1     Completed   0          5h38m
kube-system   local-path-provisioner-7c458769fb-s2xww   1/1     Running     3          5h38m
kube-system   metrics-server-86cbb8457f-ndxlz           1/1     Running     0          5h38m
default       nginx                                     1/1     Running     0          3m11s
kube-system   svclb-traefik-gb64t                       2/2     Running     0          5h38m
kube-system   traefik-6f9cbd9bd4-xlslc                  1/1     Running     0          5h38m
```

##  Custom columns

```
kubectl get pod  -A  -o=custom-columns="YZZ:.metadata.name"
YZZ
metrics-server-86cbb8457f-ndxlz
helm-install-traefik-hx29s
coredns-854c77959c-m972h
svclb-traefik-gb64t
traefik-6f9cbd9bd4-xlslc
local-path-provisioner-7c458769fb-s2xww
nginx

```

##  Overrides CMD equivalent in Dockerfile and does not modify ENTRYPOINT at all :)

```
kubectl  run webapp-green --image kodekloud/webapp-color -- --color=green
```

##  Create redis pod and serivce

```
kubectl run redis --image=redis:alpine --labels="tier=db"
kubectl  create service clusterip redis-service --tcp="6379:6379"
kubectl  edit svc redis-service

...

```

##  Create deployment

```
 kubectl create deployment webapp --image=kodekloud/webapp-color --replicas=3
deployment.apps/webapp created
controlplane $ kubectl  get pods
NAME                      READY   STATUS              RESTARTS   AGE
nginx-pod                 1/1     Running             0          9m26s
redis                     1/1     Running             0          8m23s
webapp-56847f875b-49c77   0/1     ContainerCreating   0          8s
webapp-56847f875b-tp8hl   0/1     ContainerCreating   0          8s
webapp-56847f875b-vmtzq   0/1     ContainerCreating   0          8s
```

##  Create pod with a specific container port

```
kubectl  run custom-nginx --image=nginx --port="8080"
```
##  Create deployment in specific namespace

```
kubectl  create deployment redis-deploy --namespace dev-ns --image=redis --replicas=2
deployment.apps/redis-deploy created
```

##  Create a service and pod at one shot

```
kubectl run httpd --image=httpd:alpine --namespace=default --port=80  --expose
service/httpd created
pod/httpd created
```


##  Create app with env. variable

```
kubectl  run webapp-color --image=kodekloud/webapp-color --labels="name=webapp-color" --env="APP_COLOR=green"

kubectl  create configmap webapp-config-map --from-literal=APP_COLOR=darkblue


apiVersion: v1
kind: Pod
metadata:
  labels:
    name: webapp-color
  name: webapp-color
  namespace: default
spec:
  containers:
  - image: kodekloud/webapp-color
    imagePullPolicy: Always
    name: webapp-color
    envFrom:
    - configMapRef:
        name: webapp-config-map
```

##  Create secret

```
kubectl  create secret generic db-secret --from-literal=DB_Host=sql01 --from-literal=DB_User=root --from-literal=DB_Password=password123

```

##  Security Context

```yaml

kubectl  run ubuntu-sleeper --image=ubuntu --dry-run -o yaml > pod.yaml

 cat pod.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: ubuntu-sleeper
  name: ubuntu-sleeper
spec:
  containers:
  - image: ubuntu
    name: ubuntu-sleeper
    resources: {}
    securityContext:
      runAsUser: 1010
```

##  Add Capabilities

```yaml
cat pod.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: ubuntu-sleeper
  name: ubuntu-sleeper
spec:
  containers:
  - image: ubuntu
    name: ubuntu-sleeper
    securityContext:
      runAsUser: 1010
      capabilities:
        add: ["SYS_TIME"]
```

##  Limit Range

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
spec:
  limits:
  - default:
      memory: 512Mi
    defaultRequest:
      memory: 256Mi
    type: Container
```

##  Create a pod elephant with resource requests and limits

```yaml
kubectl  run elephant --image=polinux/stress --requests="memory=5Mi" --limits="memory=20Mi"
```
##  Create a pod elephant with resource requests and limits plus command and args

```yaml
kubectl  run elephant --image=polinux/stress --requests="memory=5Mi" --limits="memory=20Mi" --command -- stress  --vm 1 --vm-bytes 15M --vm-hang 1
```
