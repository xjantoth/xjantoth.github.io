---
title: "How to start K3S on Raspberry Pi3"
date: "2021-12-30T16:09:28+0100"
lastmod: "2021-12-30T16:09:28+0100"
draft: false
author: "Jan Toth"
description: "How to start K3S on Raspberry Pi3"
image: "/assets/images/blog/raspberrypi/raspberrypi.png"

tags: ['raspberry', 'k3s', 'k8s']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

https://blog.alexellis.io/test-drive-k3s-on-raspberry-pi/

```
cat /boot/config.txt  | grep "arm_64bit"
arm_64bit=1

vim /boot/cmdline.txt
...
cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory
...
:wq!


export K3S_KUBECONFIG_MODE="644"
export INSTALL_K3S_EXEC=" --no-deploy servicelb --no-deploy traefik"

curl -sfL https://get.k3s.io | sh -

curl -L https://get.helm.sh/helm-v3.2.4-linux-arm64.tar.gz | tar -xvzf - --strip-components=1 -C /usr/local/bin/ linux-arm64/helm
```
