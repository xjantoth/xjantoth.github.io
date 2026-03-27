---
title: "SSH to AWS instances - use SSH tunnel 30111"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=800&h=420&fit=crop"
description: "How to ''SSH'' and open a tunnel for port 30111."

tags: ['ssh', 'aws', 'tunnel']
categories: ["AWS"]
---

How to ''SSH'' and open a tunnel for port 30111

```

ssh \
-o "IdentitiesOnly yes" \
-i  ~/.ssh/key.pem \
ec2-user@1.2.3.4 \
-L30111:127.0.0.1:30111
```
