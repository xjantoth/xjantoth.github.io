---
title: "Podman commands"
date: 2022-07-26T12:29:09+0200
lastmod: 2022-07-26T12:29:09+0200
draft: false
description: "Podman commands"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['podman', 'commands']
---

##### Assuming there are more containers running in a single Podman `pod`

* some backend service 9011
* phpMyAmdin at port 80 (interpreted by Apache2 inside container)


```
podman create --restart=always --pod=some-pod-name --name=phpmyadmin -e PMA_ABSOLUTE_URI="https://some.subdomain.com/insight/" phpmyadmin/phpmyadmin:5.2.0
```

Debugging via `tcpdump` container

```
podman run  --restart=always -it --pod=some-pod-name --name=tcpdump --entrypoint=/bin/sh kaazing/tcpdump

```

##### Useful Nginx snippet to proxy to phpMyAmdin

```
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
