---
title: "How to trust self-signed SSL/TLS certificates linux"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "cryptsetup"

image: "/assets/images/blog/linux-1.jpg"
tags: ['self-signed', 'ssl', 'tls', 'certificates', 'linux']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

How to enable system wide trust for the private Docker registry:
create the symlink:

```
ln -s /etc/pki/tls/certs/docker-registry-ca.crt  /etc/pki/ca-trust/source/anchors/
update-ca-trust
curl -v https://localhost:5000
```
RPM spec: Requires: /usr/bin/update-ca-trust Requires: ca-certificates
