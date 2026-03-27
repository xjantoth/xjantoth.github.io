---
title: Azure az behind corporate proxy
date: 2024-03-05T08:53:16+0100
lastmod: 2024-03-05T08:53:16+0100
draft: false
description: "Url that solves that problem with being behind corporate proxy."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'devopsinuse']
categories: ["Linux"]
---

## Url that solves that problem with being behind corporate proxy

https://docs.microsoft.com/en-us/cli/azure/use-cli-effectively?tabs=bash%2Cbash2


```bash
# https://docs.microsoft.com/en-us/cli/azure/use-cli-effectively?tabs=bash%2Cbash2
cat ~/Documents/proxyCA.crt >>  /usr/local/Cellar/azure-cli/2.39.0/libexec/lib/python3.10/site-packages/certifi/cacert.pem

# Latest version
brew config
cat ~/Documents/proxyCA.crt >> /opt/homebrew/Cellar/azure-cli/2.57.0/libexec/lib/python3.11/site-packages/certifi/cacert.pem
export REQUESTS_CA_BUNDLE=/opt/homebrew/Cellar/azure-cli/2.57.0/libexec/lib/python3.11/site-packages/certifi/cacert.pem
az login
```

