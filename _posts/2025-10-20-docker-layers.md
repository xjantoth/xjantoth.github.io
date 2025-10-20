---
title: "Docker layers"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Docker layers"

tags: ['docker', 'layers']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
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
