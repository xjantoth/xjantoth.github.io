---
title: "Docker push to remote registry via self signed SSL certificate"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "Docker push to remote registry via self signed https"

image: "/assets/images/blog/linux-1.jpg"
tags: ['docker', 'to', 'remote', 'registry', 'self', 'signed', 'ssl', 'certificate']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

1. ''CA (Certificate Authority)''  to your local and copy/paste it to a proper location
# download from your server

```
scp root@vm027.qa.cz....com:/etc/pki/tls/certs/docker-registry-ca.crt  .
```

2. Paste it to this location at Windows Machine

```
C:\ProgramData\docker\certs.d\ca.crt
```

3. There is a good chance that folder certs.d does not exist yet ( please create it)

4. Restart docker at your Windows machine

5. Tag image by remote server name

```
docker tag some-docker-image <vm027.qa.cz.company.com>:5000/some-docker-image
```

6. Push it to a remote registry

```
docker push <vm027.qa.cz.company.com>:5000/some-docker-image
```
