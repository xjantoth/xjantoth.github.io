---
title: "SSH to AWS instances - use SSH tunnel 30111"
date: "2022-01-04T13:36:26+0100"
lastmod: "2022-01-04T13:36:26+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/aws-1.jpg"
description: "SSH to AWS instances - use SSH tunnel 30111"

tags: ['ssh', 'to', 'aws', 'instances', 'use', 'ssh', 'tunnel']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

How to ''SSH'' and open a tunnel for port 30111

```

ssh \
-o "IdentitiesOnly yes" \
-i  ~/.ssh/key.pem \
ec2-user@1.2.3.4 \
-L30111:127.0.0.1:30111
```
