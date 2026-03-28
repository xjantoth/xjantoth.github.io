---
title: Use corporate proxy certificate
date: 2025-07-30T11:16:59+0200
lastmod: 2025-07-30T11:16:59+0200
draft: false
description: "In case you are behind corporate proxy - the following commands might help."
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'devopsinuse', 'cert', 'ssl']
categories: ["Networking"]
---


In case you are behind a corporate proxy, the following commands might help.

These environment variables tell Python-based tools (pip, requests, httplib2) and curl to use the CA bundle provided by the `certifi` package. This is the quickest way to make most CLI tools trust your corporate proxy certificate without modifying system-level CA stores.

```bash
export CERT_PATH=$(python3 -m certifi)
export SSL_CERT_FILE=${CERT_PATH}
export CURL_CA_BUNDLE=${CERT_PATH}
export REQUESTS_CA_BUNDLE=${CERT_PATH}
export HTTPLIB2_CA_CERTS=${CERT_PATH}
```
