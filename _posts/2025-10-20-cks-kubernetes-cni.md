---
title: "CKS Kubernetes CNI"
date: 2022-08-03T20:57:04+0200
lastmod: 2022-08-03T20:57:04+0200
draft: false
description: "CKS Kubernetes CNI"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['cks', 'kubernetes', 'cni']
---

## Container infor passed by kubelet to stdin of CNI bash plugin

```bash
CNI_CONTAINERID=b552f9...
CNI_IFNAME=eth0
CNI_COMMAND=ADD
CNI_NETNS=/proc/6137/ns/net
```


# interesting fact
ls -sfT $CNI_NETNS /var/run/netns/$CNI_CONTAINERID

```bash
![Image](/assets/images/blog/cni-1.png)
![Image](/assets/images/blog/cni-2.png)
![Image](/assets/images/blog/cni-3.png)
![Image](/assets/images/blog/cni-4.png)
![Image](/assets/images/blog/cni-5.png)
![Image](/assets/images/blog/cni-6.png)
![Image](/assets/images/blog/cni-7.png)
![Image](/assets/images/blog/cni-8.png)
![Image](/assets/images/blog/cni-9.png)
![Image](/assets/images/blog/cni-10.png)
```

#### How to create client/server namespace and run python webserver

https://www.redhat.com/sysadmin/net-namespaces

```bash
export namespace1=client
export namespace2=server
export command='python3 -m http.server'
export ip_address1="10.10.10.10/24"
export ip_address2='10.10.10.20/24'
export interface1=veth-client
export interface2=veth-server

ip netns add $namespace1
ip netns add $namespace2
ip link add ptp-$interface1 type veth peer name ptp-$interface2
ip link set ptp-$interface1 netns $namespace1
ip link set ptp-$interface2 netns $namespace2
ip netns exec $namespace1 ip addr add $ip_address1 dev ptp-$interface1
ip netns exec $namespace2 ip addr add $ip_address2 dev ptp-$interface2
ip netns exec $namespace1 ip link set dev ptp-$interface1 up
ip netns exec $namespace2 ip link set dev ptp-$interface2 up
ip netns exec $namespace2 $command &
ip netns pids $namespace2
ip netns ls
ls -ltr /proc/*/ns/net | grep 15035

root@tf-srv-gallant-shaw:~# ip netns exec $namespace1 curl 10.10.10.20:8000

```
