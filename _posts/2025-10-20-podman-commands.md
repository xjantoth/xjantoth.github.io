---
title: "Podman commands"
date: 2022-07-26T12:29:09+0200
lastmod: 2022-07-26T12:29:09+0200
draft: false
description: "Assuming there are more containers running in a single Podman `pod`."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['podman', 'commands']
categories: ["Kubernetes"]
---

##### Assuming there are more containers running in a single Podman `pod`

* some backend service on port 9011
* phpMyAdmin at port 80 (interpreted by Apache2 inside container)

This command creates a phpMyAdmin container inside an existing Podman pod. The `PMA_ABSOLUTE_URI` environment variable tells phpMyAdmin the base URL it is served from, which is needed when running behind a reverse proxy.

```bash
podman create --restart=always --pod=some-pod-name --name=phpmyadmin -e PMA_ABSOLUTE_URI="https://some.subdomain.com/insight/" phpmyadmin/phpmyadmin:5.2.0
```

You can attach a tcpdump container to the same pod for network debugging. Since all containers in a Podman pod share the same network namespace, tcpdump will see all traffic.

```bash
podman run  --restart=always -it --pod=some-pod-name --name=tcpdump --entrypoint=/bin/sh kaazing/tcpdump

```

##### Useful Nginx snippet to proxy to phpMyAdmin

This Nginx server block proxies API requests to a backend service and serves a frontend SPA from static files. The `/insight/` location block reverse-proxies requests to the phpMyAdmin container running on port 80 within the same pod.

```nginx
server {
    listen       8091;
    server_name some.subdomain.com;

    location /api/ {
        proxy_pass "http://127.0.0.1:8011/";

        # WebSocket support (nginx 1.4)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # phpMyAdmin section
    location ~ ^/insight/ {
        rewrite ^/insight(/.*)$ $1 break;
        proxy_pass http://127.0.0.1;
    }

}
```
