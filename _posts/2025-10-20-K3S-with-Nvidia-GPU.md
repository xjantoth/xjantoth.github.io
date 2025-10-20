---
title: "K3S with Nvidia GPU"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-1.jpg"
description: "K3S with Nvidia GPU"

tags: ["kubernetes", "install", "k3s", "raspberry", "gpu", "nvidia"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
mkdir $HOME/.kube/
curl -sfL https://get.k3s.io | sh -s - --docker --write-kubeconfig-mode 644 --write-kubeconfig $HOME/.kube/config
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.6.0/nvidia-device-plugin.yml

cat pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nvidia-smi
spec:
  restartPolicy: OnFailure
  containers:
  - name: nvidia-smi
    image: nvidia/cuda
    args:
    - "nvidia-smi"
    resources:
      limits:
        nvidia.com/gpu: 1


kubectl apply -f pod.yaml

kubectl  logs -f  nvidia-smi
Sat Sep 26 13:15:22 2020
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 450.51.06    Driver Version: 450.51.06    CUDA Version: 11.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla K80           On   | 00000000:00:1E.0 Off |                    0 |
| N/A   39C    P8    30W / 149W |      0MiB / 11441MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+


```
