---
title: "Access Google's metadata"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Access Google's metadata — practical walkthrough with examples."

tags: ['access', "google's", 'metadata']
categories: ["DevOps"]
---

## Access Google's metadata

The following command queries the Google Cloud instance metadata server to retrieve the instance ID. This is useful when running on GCE VMs and you need to programmatically identify the current instance. The `Metadata-Flavor: Google` header is required by the metadata server.

```bash
curl http://metadata.google.internal/computeMetadata/v1/instance/id -H "Metadata-Flavor: Google"
```
