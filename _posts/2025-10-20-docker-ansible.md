---
title: "Docker ansible"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1518432031352-d6fc5c10da5a?w=800&h=420&fit=crop"
description: "How to build, push, and run a Docker image with Ansible pre-installed for ML infrastructure automation."

tags: ['ml', 'docket', 'ansible']
categories: ["Automation"]
---

These commands log in to Docker Hub, push a custom Ansible image, and then run a container from that image with a local project directory mounted as a volume. This is useful for running Ansible playbooks in a consistent, containerized environment.

```bash
export CI_REGISTRY=docker.io
docker login -u "devopsinuse" -p "..." $CI_REGISTRY
docker push devopsinuse/ansible-ml:v2.9.2

docker run -it -v /home/jantoth/Documents/sbx/ml/k3s:/home/ml-ansible   -w /home/ml-ansible ansible-ml:v2.9.2.1 sh
```
