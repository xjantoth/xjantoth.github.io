---
title: "Linux Namespaces"
date: 2022-01-14T13:38:26+01:00
lastmod: 2022-01-14T13:38:33+01:00
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Linux Namespaces"

tags: ['linux', 'namespaces']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

### **Namespaces isolates processess**

- **restricts what processes can see**.

* PID namespace:
    - isolates processess from each other
    - one process cannot see others
    - process ID 10 can exist multiple times, once in every namespace

* Mount namespace:
    - resticts access to filesystem

* Network namespace:
    - separates network traffic

* User namespace:
    - user 0 can exist in every namespace and all of them are different

### **Cgroups**
- resticts the resource usage of processes (RAM, disk, CPU)



### Difference between user and kernel space in Linux

![Image](/assets/images/blog/kernel-user-spaces.png)

### Container tools

Take a look at some container tools:

![Image](/assets/images/blog/container-tools.png)


### Check how process in containers can be islolated from each other.

```
docker run --name c1 -d ubuntu sh -c 'sleep 1d'
docker run --name c2 -d ubuntu sh -c 'sleep 999d'
docker exec c1 ps aux
docker exec c2 ps aux

docker rm c2 --force

# now c2 can see processes from container c1
docker run --name c2 --pid=container:c1 -d ubuntu sh -c 'sleep 999d'
docker exec c2 ps aux
