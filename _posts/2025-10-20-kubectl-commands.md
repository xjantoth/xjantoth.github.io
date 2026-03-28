---
title: "Kubectl Commands"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "kubectl commands — practical walkthrough with examples."

tags: ['kubectl', 'commands']
categories: ["Kubernetes"]
---

##  kubectl sort by

Sort all pods across namespaces alphabetically by their name using the `--sort-by` flag with a JSONPath expression.

```bash
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

Use custom columns to display only specific fields from the pod metadata. This is useful for creating concise, targeted output.

```bash
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

##  Override CMD equivalent in Dockerfile without modifying ENTRYPOINT

The double dash `--` separates kubectl arguments from the container arguments. Everything after `--` is passed as the CMD to the container, overriding the Dockerfile CMD but leaving ENTRYPOINT intact.

```bash
kubectl  run webapp-green --image kodekloud/webapp-color -- --color=green
```

##  Create redis pod and service

Create a Redis pod with labels and a ClusterIP service to expose it. After creating the service, you may need to edit the selector to match the pod labels.

```bash
kubectl run redis --image=redis:alpine --labels="tier=db"
kubectl  create service clusterip redis-service --tcp="6379:6379"
kubectl  edit svc redis-service

...

```

##  Create deployment

Create a deployment with three replicas. Kubernetes will schedule the pods across available nodes.

```bash
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

The `--port` flag sets the container port in the pod spec. This does not expose the port externally; it only declares which port the container listens on.

```bash
kubectl  run custom-nginx --image=nginx --port="8080"
```
##  Create deployment in specific namespace

Use `--namespace` to place a deployment in a specific namespace. The deployment and its pods will all reside in that namespace.

```bash
kubectl  create deployment redis-deploy --namespace dev-ns --image=redis --replicas=2
deployment.apps/redis-deploy created
```

##  Create a service and pod in one shot

The `--expose` flag creates both a pod and a matching ClusterIP service in a single command.

```bash
kubectl run httpd --image=httpd:alpine --namespace=default --port=80  --expose
service/httpd created
pod/httpd created
```


##  Create app with environment variable

You can set environment variables directly with `--env`, or use a ConfigMap for more flexible configuration. The pod spec below shows how to inject all keys from a ConfigMap using `envFrom`.

```bash
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

Create a generic secret from literal key-value pairs. These values are base64-encoded and stored in the cluster.

```bash
kubectl  create secret generic db-secret --from-literal=DB_Host=sql01 --from-literal=DB_User=root --from-literal=DB_Password=password123

```

##  Security Context

Set a security context on a pod to run the container as a specific user. The `runAsUser` field specifies the UID that the container process will run as.

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

Linux capabilities can be added to a container's security context. This example adds the `SYS_TIME` capability, allowing the container to modify the system clock.

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

A LimitRange sets default resource requests and limits for containers in a namespace. If a pod does not specify memory requests or limits, these defaults are applied.

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

##  Create a pod with resource requests and limits

Create a stress-test pod with explicit memory requests and limits.

```bash
kubectl  run elephant --image=polinux/stress --requests="memory=5Mi" --limits="memory=20Mi"
```

##  Create a pod with resource requests, limits, and custom command

Add `--command --` to override the container entrypoint. The stress tool arguments control how much memory the pod attempts to allocate.

```bash
kubectl  run elephant --image=polinux/stress --requests="memory=5Mi" --limits="memory=20Mi" --command -- stress  --vm 1 --vm-bytes 15M --vm-hang 1
```
