---
title: "Nvidia Jetson installation"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Nvidia Jetson installation"

tags: ['ml', 'install', 'k3s', 'raspberry', 'gpu', 'nvidia', 'jetson']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

##  Download SD card image
https://developer.download.nvidia.com/assets/embedded/downloads/jetson-nano-4gb-jp441-sd-card-image/jetson-nano-4gb-jp441-sd-card-image.zip

##  Create SD card for NVIDIA Jetson Nano

```sh
unzip -p  ~/Downloads/jetson-nano-4gb-jp441-sd-card-image.zip | sudo /bin/dd of=/dev/mmcblk0  bs=1M status=progress
```


##  update docker runtime

```
sudo cp /etc/docker/daemon.json  /etc/docker/daemon.json.orig
ubuntu@k3s-jetson-1:~$
ubuntu@k3s-jetson-1:~$
ubuntu@k3s-jetson-1:~$ sudo vim /etc/docker/daemon.json
ubuntu@k3s-jetson-1:~$ cat  /etc/docker/daemon.json
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    },
    "default-runtime": "nvidia"
}

sudo systemctl restart docker

ubuntu@k3s-jetson-1:~$ sudo docker info | grep Def
Default Runtime: nvidia

```

##  try to run docker docntainer with tensorflow

```
sudo docker run -it --rm --runtime nvidia --network host nvcr.io/nvidia/l4t-tensorflow:r32.4.3-tf2.2-py3 python3

Python 3.6.9 (default, Apr 18 2020, 01:56:04)
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>>
>>> 1
1
>>> 2
2
>>> import tensorflow as tf
2020-11-19 12:04:09.268672: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcudart.so.10.2
>>> print(tf.__version__)
2.2.0


>>> tf.config.list_physical_devices('GPU')
2020-11-19 12:05:17.191282: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcuda.so.1
2020-11-19 12:05:17.206274: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:948] ARM64 does not support NUMA - returning NUMA node zero
2020-11-19 12:05:17.206430: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1561] Found device 0 with properties:
pciBusID: 0000:00:00.0 name: NVIDIA Tegra X1 computeCapability: 5.3
coreClock: 0.9216GHz coreCount: 1 deviceMemorySize: 3.87GiB deviceMemoryBandwidth: 194.55MiB/s
2020-11-19 12:05:17.206513: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcudart.so.10.2
2020-11-19 12:05:17.267906: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcublas.so.10
2020-11-19 12:05:17.348069: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcufft.so.10
2020-11-19 12:05:17.471141: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcurand.so.10
2020-11-19 12:05:17.655922: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcusolver.so.10
2020-11-19 12:05:17.739489: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcusparse.so.10
2020-11-19 12:05:17.741373: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcudnn.so.8
2020-11-19 12:05:17.742026: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:948] ARM64 does not support NUMA - returning NUMA node zero
2020-11-19 12:05:17.742338: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:948] ARM64 does not support NUMA - returning NUMA node zero
2020-11-19 12:05:17.742455: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1703] Adding visible gpu devices: 0
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]

```


```
 cat pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: tensorflow
spec:
  containers:
  - name: tf
    image: nvcr.io/nvidia/l4t-tensorflow:r32.4.3-tf2.2-py3
    command: [ "/bin/bash", "-c", "--" ]
    args: [ "while true; do sleep 30; done;" ]

ubuntu@k3s-jetson-1:~$ logout
kubectl apply -f pod.yaml
pod/tensorflow created

kubectl get pods
NAME         READY   STATUS    RESTARTS   AGE
tensorflow   1/1     Running   0          5s

kubectl get pods -o wide
NAME         READY   STATUS    RESTARTS   AGE   IP          NODE           NOMINATED NODE   READINESS GATES
tensorflow   1/1     Running   0          9s    10.42.1.4   k3s-jetson-1   <none>           <none>


```
