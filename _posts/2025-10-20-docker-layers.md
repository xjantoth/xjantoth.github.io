---
title: "Docker layers"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1605745341112-85968b19335b?w=800&h=420&fit=crop"
description: "Multi-stage Dockerfile example: build a Go application in Ubuntu, then copy the binary into a minimal Alpine image with a non-root user."

tags: ['docker', 'layers']
categories: ["Docker"]
---

This multi-stage Dockerfile first builds a Go application in an Ubuntu-based stage, then copies just the compiled binary into a minimal Alpine image. The final stage removes all binaries from `/bin`, creates a non-root user, and runs the application as that user for improved security.

```dockerfile
cat  Dockerfile
FROM ubuntu
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get install golang-go -y
COPY app.go .
RUN CGO_ENABLED=0 go build app.go


FROM alpine:3.12.1
RUN chmod a-w /etc && \
  addgroup -S appgroup && adduser -S appuser -G appgroup -h /home/appuser && \
  rm -rf /bin/*
COPY --from=0 /app /home/appuser
USER appuser
CMD ["/home/appuser/app"]

```
