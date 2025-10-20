---
title: Use corporate proxy certificate
date: 2025-07-30T11:16:59+0200
lastmod: 2025-07-30T11:16:59+0200
draft: false
description: Use corporate proxy certificate
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ["bash", "devopsinuse", "cert", "ssl"]
---


In case you are behind corporate proxy - the following commands might help.

```bash
export CERT_PATH=$(python3 -m certifi)
export SSL_CERT_FILE=${CERT_PATH}
export CURL_CA_BUNDLE=${CERT_PATH}
export REQUESTS_CA_BUNDLE=${CERT_PATH}
export HTTPLIB2_CA_CERTS=${CERT_PATH}
```
