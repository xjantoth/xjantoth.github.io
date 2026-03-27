---
title: "Securing docker daemon"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1605745341112-85968b19335b?w=800&h=420&fit=crop"
description: "Securing docker daemon — practical walkthrough with examples."

tags: ['securing', 'docker', 'daemon']
categories: ["Docker"]
---

**Best practices''

```
export DOCKER_HOST=192.1681.2 <---- insecure
/var/run/docker.sock   < --- secure
export DOCKER_TLS=true
```
