---
title: "Docker layers"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1605745341112-85968b19335b?w=800&h=420&fit=crop"
description: "Docker layers — practical walkthrough with examples."

tags: ['docker', 'layers']
categories: ["Docker"]
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
