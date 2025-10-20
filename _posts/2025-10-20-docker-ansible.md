---
title: "Docker ansible"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "docker ansible"

tags: ["ml", "docket", "ansible"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
export CI_REGISTRY=docker.io
docker login -u "devopsinuse" -p "..." $CI_REGISTRY
docker push devopsinuse/ansible-ml:v2.9.2

docker run -it -v /home/jantoth/Documents/sbx/ml/k3s:/home/ml-ansible   -w /home/ml-ansible ansible-ml:v2.9.2.1 sh
```
