---
title: "SSH to AWS instances - use SSH tunnel 30111"
date: "2022-01-04T13:36:26+0100"
lastmod: "2022-01-04T13:36:26+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=800&h=420&fit=crop"
description: "How to SSH into an AWS EC2 instance and open a local port tunnel for port 30111."

tags: ['ssh', 'aws', 'instances', 'tunnel']
categories: ["AWS"]
---

How to SSH and open a tunnel for port 30111.

The following command connects to an EC2 instance while establishing a local port forward. This maps local port 30111 to port 30111 on the remote host, which is useful for accessing services like NodePort-exposed Kubernetes workloads.

```bash
ssh \
-o "IdentitiesOnly yes" \
-i  ~/.ssh/key.pem \
ec2-user@1.2.3.4 \
-L30111:127.0.0.1:30111
```
