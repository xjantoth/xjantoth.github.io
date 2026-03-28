---
title: "How to trust self-signed SSL/TLS certificates linux"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "How to enable system-wide trust for self-signed SSL/TLS certificates on Linux, useful for private Docker registries and internal services."

image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=420&fit=crop"
tags: ['ssl', 'tls', 'certificates', 'linux']
categories: ["Networking"]
---

How to enable system-wide trust for the private Docker registry:
create the symlink:

To add a self-signed CA certificate to the system trust store on RHEL/CentOS, create a symlink from your certificate into the anchors directory and then run `update-ca-trust`. After that, tools like `curl` will trust the certificate without requiring the `--insecure` flag.

```bash
ln -s /etc/pki/tls/certs/docker-registry-ca.crt  /etc/pki/ca-trust/source/anchors/
update-ca-trust
curl -v https://localhost:5000
```

RPM spec: Requires: /usr/bin/update-ca-trust Requires: ca-certificates
