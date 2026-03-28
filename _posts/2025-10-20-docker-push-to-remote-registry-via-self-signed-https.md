---
title: "Docker push to remote registry via self signed SSL certificate"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "How to push Docker images to a remote registry that uses a self-signed SSL certificate by installing the CA cert locally."

image: "https://images.unsplash.com/photo-1605745341112-85968b19335b?w=800&h=420&fit=crop"
tags: ['docker', 'to', 'remote', 'registry', 'self', 'signed', 'ssl', 'certificate']
categories: ["Docker"]
---

1. Download the CA (Certificate Authority) certificate from your server to your local machine.

```bash
scp root@vm027.qa.cz....com:/etc/pki/tls/certs/docker-registry-ca.crt  .
```

2. Paste it to this location on your Windows machine.

```
C:\ProgramData\docker\certs.d\ca.crt
```

3. There is a good chance that folder certs.d does not exist yet ( please create it)

4. Restart docker at your Windows machine

5. Tag the image with the remote server name and port so Docker knows where to push it.

```bash
docker tag some-docker-image <vm027.qa.cz.company.com>:5000/some-docker-image
```

6. Push the tagged image to the remote registry.

```bash
docker push <vm027.qa.cz.company.com>:5000/some-docker-image
```
