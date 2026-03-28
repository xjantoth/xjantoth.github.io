---
title: "How to use X-Hook-Signature for simple webhook verification"
date: 2026-01-16T15:51:17:+0100
lastmod: 2026-01-16T15:51:17:+0100
draft: false
description: "How to use X-Hook-Signature for HMAC-SHA512 webhook verification when writing a Python web server."
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: []
categories: ["DevOps"]
---

## How to use X-Hook-Signature when writing a Python web server

When building a webhook receiver in Python, you often need to verify the authenticity of incoming requests. The `X-Hook-Signature` header contains an HMAC-SHA512 digest of the request body, signed with a shared secret. The following curl command demonstrates how to compute the signature and send it alongside the payload, which your server can then verify.

```bash
curl -H "X-Hook-Signature: $(echo -n '{"key":"value"}' | openssl dgst -sha512 -hmac "secret" -hex | cut -d" " -f2)"  \
  -H "Content-Type: application/json" -d '{"key":"value"}'  \
  http://127.0.0.1:5000/create-group
```
