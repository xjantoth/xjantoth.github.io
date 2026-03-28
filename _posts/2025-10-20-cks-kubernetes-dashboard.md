---
title: "Kubernetes dashboard"
date: 2022-02-21T13:43:50+01:00
lastmod: 2022-02-21T13:43:43+01:00
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "How to install and configure the Kubernetes dashboard, including SSH tunneling, token retrieval, and enabling insecure HTTP access."

tags: ['kubernetes', 'dashboard']
categories: ["Kubernetes"]
---

###### Kubectl proxy

* creates a proxy server between localhost and the Kubernetes API Server
* uses connection as configured in the kubeconfig
* Run `kubectl proxy` command at your master node cks-master

![Image](/assets/images/blog/dashboard-1.png)


###### Kubectl port-forward

![Image](/assets/images/blog/dashboard-2.png)


###### Install Kubernetes dashboard

Deploy the Kubernetes dashboard using the official recommended manifest. This creates the dashboard Deployment, Service, and required RBAC resources in the `kubernetes-dashboard` namespace.

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.5.0/aio/deploy/recommended.yaml
```

###### Create **SSH** tunnel to cks-master

```bash
ssh -i  ~/.ssh/google_compute_engine -L8001:127.0.0.1:8001 jantoth@35.198.101.56
```
###### Find a **token** belonging to kubernetes-dashboard **serviceaccount**

```bash
kubectl  get secret kubernetes-dashboard-token-c7j68 -n kubernetes-dashboard  -ojsonpath='{.data.token}' | base64 -d
```

###### How to enable insecure HTTP at kubernetes dashboard


To enable insecure HTTP access, edit the dashboard Deployment to disable auto-generated certificates and add the `--insecure-port=9090` flag. You also need to update the Service to match the new port.

```yaml
hugo % k edit deployments.apps -n kubernetes-dashboard kubernetes-dashboard
deployment.apps/kubernetes-dashboard edited

...
    matchLabels:
      k8s-app: kubernetes-dashboard
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        k8s-app: kubernetes-dashboard
    spec:
      containers:
      - args:
        # - --auto-generate-certificates            < ------- disable this option !!!
        - --namespace=kubernetes-dashboard
        - --insecure-port=9090                      < ------- add this option !!!
        image: kubernetesui/dashboard:v2.5.0
        imagePullPolicy: Always
        livenessProbe:

        ...
        PLUS adjust readiness and livenessProbe ...
        ...


# edit service too
k edit svc -n kubernetes-dashboard kubernetes-dashboard
apiVersion: v1
kind: Service
metadata:
  ...
  ...
  ports:
  - nodePort: 30222
    port: 9090
    protocol: TCP
    targetPort: 9090
  selector:
    k8s-app: kubernetes-dashboard
  sessionAffinity: None
  type: NodePort

```
