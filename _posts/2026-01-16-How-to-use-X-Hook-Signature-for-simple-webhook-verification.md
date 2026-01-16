---
title: "How to use X-Hook-Signature for simple webhook verification"
date: 2026-01-16T15:51:17:+0100
lastmod: 2026-01-16T15:51:17:+0100
draft: false
description: "How to use X-Hook-Signature for simple webhook verification"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: []
---


How to use X-Hook-Signature when writing Python web server

```bash
curl -H "X-Hook-Signature: $(echo -n '{"key":"value"}' | openssl dgst -sha512 -hmac "secret" -hex | cut -d" " -f2)"  \
  -H "Content-Type: application/json" -d '{"key":"value"}'  \
  http://127.0.0.1:5000/create-group

```
