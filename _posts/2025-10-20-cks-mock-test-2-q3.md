---
title: "CKS Mock test 2 - Q3"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "CKS mock test 2, question 3: Secure a pod by disabling automatic mounting of the service account secret token using automountServiceAccountToken."

tags: ['cks', 'mock', 'q3']
categories: ["Kubernetes"]
---

**3. A pod has been created in the gamma namespace using a service account called cluster-view. This service account has been granted additional permissions as compared to the default service account and can view resources cluster-wide on this Kubernetes cluster. While these permissions are important for the application in this pod to work, the secret token is still mounted on this pod.


Secure the pod in such a way that the secret token is no longer mounted on this pod. You may delete and recreate the pod.

The key change is setting `automountServiceAccountToken: false` in the pod spec. This prevents Kubernetes from mounting the service account token into the pod, reducing the attack surface while still associating the pod with the `cluster-view` service account.

```yaml
cat 3.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: apps-cluster-dash
  name: apps-cluster-dash
  namespace: gamma
spec:
  automountServiceAccountToken: false
  containers:
  - image: nginx
    imagePullPolicy: Always
    name: apps-cluster-dash
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: node01
  preemptionPolicy: PreemptLowerPriority
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: cluster-view
  serviceAccountName: cluster-view
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
```
