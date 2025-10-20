---
title: "CKS container runtimes"
date: 2022-05-18T11:41:55+0200
lastmod: 2022-05-18T11:41:55+0200
draft: false
description: "CKS container runtimes"
image: "/assets/images/blog/container-1.png"
author: "Jan Toth"
tags: ['cks', 'container', 'runtimes']
---

![Image](/assets/images/blog/container-1.png)
![Image](/assets/images/blog/container-2.png)
![Image](/assets/images/blog/container-3.png)
![Image](/assets/images/blog/container-4.png)
![Image](/assets/images/blog/container-5.png)

```bash
# go inside of a container and call
root@scw-k8s:~# k exec -it pod -- sh
/ # uname -r
5.4.0-96-generic

# step outside of a container and call
root@scw-k8s:~# strace uname -n
execve("/bin/uname", ["uname", "-n"], 0x7fff04c24c98 /* 24 vars */) = 0
brk(NULL)                               = 0x55bfd0cf3000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=23538, ...}) = 0
mmap(NULL, 23538, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f6e56b83000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\240\35\2\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0755, st_size=2030928, ...}) = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f6e56b81000
mmap(NULL, 4131552, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f6e5656f000
mprotect(0x7f6e56756000, 2097152, PROT_NONE) = 0
mmap(0x7f6e56956000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1e7000) = 0x7f6e56956000
mmap(0x7f6e5695c000, 15072, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f6e5695c000
close(3)                                = 0
arch_prctl(ARCH_SET_FS, 0x7f6e56b82540) = 0
mprotect(0x7f6e56956000, 16384, PROT_READ) = 0
mprotect(0x55bfced96000, 4096, PROT_READ) = 0
mprotect(0x7f6e56b89000, 4096, PROT_READ) = 0
...
```

###### Katacontainers

Katacontainers create a very lightweight VM with a separate kernel (quite different than a traditional containers)
Strong separation layer!
Using QEUM as default (needs virtualization, like neasted virtualisztion)

![Image](/assets/images/blog/container-6.png)

###### gVisor

* user-space kernel for containers (might be confusing)
* adds another layer of separation
* not hypervisor or VM based
* **simulates kernel syscalls** with limited functionality (in golang)
* runs in a user space separated from a linux kernel
* runtime is called `runsc`


![Image](/assets/images/blog/container-7.png)
![Image](/assets/images/blog/container-8.png)


```
#!/usr/bin/env bash
# IF THIS FAILS then you can try to change the URL= further down from specific to the latest release
# https://gvisor.dev/docs/user_guide/install


# gvisor
sudo apt-get update && \
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common


# install from web
(
  set -e
  ARCH=$(uname -m)
  URL=https://storage.googleapis.com/gvisor/releases/release/20210806/${ARCH}
  # URL=https://storage.googleapis.com/gvisor/releases/release/latest/${ARCH} # TRY THIS URL INSTEAD IF THE SCRIPT DOESNT WORK FOR YOU
  wget ${URL}/runsc ${URL}/runsc.sha512 \
    ${URL}/containerd-shim-runsc-v1 ${URL}/containerd-shim-runsc-v1.sha512
  sha512sum -c runsc.sha512 \
    -c containerd-shim-runsc-v1.sha512
  rm -f *.sha512
  chmod a+rx runsc containerd-shim-runsc-v1
  sudo mv runsc containerd-shim-runsc-v1 /usr/local/bin
)


# containerd enable runsc
cat > /etc/containerd/config.toml <<EOF
disabled_plugins = []
imports = []
oom_score = 0
plugin_dir = ""
required_plugins = []
root = "/var/lib/containerd"
state = "/run/containerd"
version = 2

[plugins]
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runsc]
    runtime_type = "io.containerd.runsc.v1"

  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
      base_runtime_spec = ""
      container_annotations = []
      pod_annotations = []
      privileged_without_host_devices = false
      runtime_engine = ""
      runtime_root = ""
      runtime_type = "io.containerd.runc.v2"

      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
        BinaryName = ""
        CriuImagePath = ""
        CriuPath = ""
        CriuWorkPath = ""
        IoGid = 0
        IoUid = 0
        NoNewKeyring = false
        NoPivotRoot = false
        Root = ""
        ShimCgroup = ""
        SystemdCgroup = true
EOF

systemctl restart containerd
```

Then you can create a `runtimeClass` and pod using that particular runtimeClass


```
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
```

Create a pod itself

```
---
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: gvisor
  name: gvisor
spec:
  runtimeClassName: gvisor
  containers:
    - image: nginx
      name: gvisor
      resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
```
