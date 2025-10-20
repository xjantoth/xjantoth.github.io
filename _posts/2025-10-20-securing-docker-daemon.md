---
title: "Securing docker daemon"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Securing docker daemon"

tags: ['securing', 'docker', 'daemon']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

**Best practices''

```
export DOCKER_HOST=192.1681.2 <---- insecure
/var/run/docker.sock   < --- secure
export DOCKER_TLS=true
```
