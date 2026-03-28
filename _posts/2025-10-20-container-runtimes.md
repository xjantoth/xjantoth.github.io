---
title: "Container Runtimes"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1605745341112-85968b19335b?w=800&h=420&fit=crop"
description: "Running containers with alternative runtimes such as Kata Containers and gVisor (runsc) using Docker."

tags: ['container', 'runtimes']
categories: ["Docker"]
---

Docker supports alternative container runtimes through the `--runtime` flag. Kata Containers runs each container in a lightweight VM for stronger isolation, while gVisor (runsc) intercepts system calls in user space to reduce the kernel attack surface.

```bash
docker run --runtime kata  -d nginx
docker run --runtime runsc -d nginx
```
