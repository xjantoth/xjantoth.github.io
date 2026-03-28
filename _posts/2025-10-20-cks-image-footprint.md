---
title: "CKS Image Footprint"
date: 2022-06-04T13:09:33+0200
lastmod: 2022-06-04T13:09:33+0200
draft: false
description: "Best practices for reducing Docker image footprint: multi-stage builds, non-root users, shell removal, and read-only filesystems."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['cks', 'image', 'footprint']
categories: ["Kubernetes"]
---

* run specific version
* do not run as root
* no shell
* read-only filesystem

This would be an ideal example of a Dockerfile using a multi-stage build. The first stage compiles a Go application, and the second stage copies only the binary into a minimal Alpine image with a non-root user and no shell binaries.

```dockerfile
# build container stage 1
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y golang-go=2:1.13~1ubuntu2
COPY app.go .
RUN pwd
RUN CGO_ENABLED=0 go build app.go

# app container stage 2
FROM alpine:3.12.0
RUN addgroup -S appgroup && adduser -S appuser -G appgroup -h /home/appuser
RUN rm -rf /bin/*
COPY --from=0 /app /home/appuser/
USER appuser
CMD ["/home/appuser/app"]
```


![Image](/assets/images/blog/fi-1.png)
![Image](/assets/images/blog/fi-2.png)
![Image](/assets/images/blog/fi-3.png)

```go
// app.go
package main

import (
    "fmt"
    "time"
    "os/user"
)

func main () {
    user, err := user.Current()
    if err != nil {
        panic(err)
    }

    for {
        fmt.Println("user: " + user.Username + " id: " + user.Uid)
        time.Sleep(1 * time.Second)
    }
}
```

Then write your `Dockerfile` but you will see that this simple app will have rather large docker image ~700MB (overkill).


```dockerfile
FROM ubuntu
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y golang-go
COPY app.go .
RUN CGO_ENABLED=0 go build app.go
CMD ["./app"]
```

Build a docker image


```bash
podman build -t app:latest .
```


Let's try to lower image size a bit by **multi-stage build**

```dockerfile
FROM ubuntu
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y golang-go
COPY app.go .
RUN CGO_ENABLED=0 go build app.go

FROM alpine
COPY --from=0 /app .
CMD ["./app"]
```
