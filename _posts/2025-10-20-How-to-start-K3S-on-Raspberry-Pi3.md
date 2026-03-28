---
title: "How to start K3S on Raspberry Pi3"
date: "2021-12-30T16:09:28+0100"
lastmod: "2021-12-30T16:09:28+0100"
draft: false
author: "Jan Toth"
description: "Step-by-step guide to installing and running K3S on a Raspberry Pi 3, including cgroup configuration and Helm installation."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"

tags: ['raspberry', 'k3s', 'k8s']
categories: ["Kubernetes"]
---

Reference: https://blog.alexellis.io/test-drive-k3s-on-raspberry-pi/

Before installing K3S, you need to enable 64-bit mode and cgroups on the Raspberry Pi. Verify the `arm_64bit` setting in `/boot/config.txt` and add the required cgroup kernel parameters to `/boot/cmdline.txt`. After rebooting, set environment variables to configure kubeconfig permissions and disable unnecessary components, then run the K3S installer. Finally, install Helm for managing Kubernetes packages.

```bash
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
