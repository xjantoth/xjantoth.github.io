---
title: "Grafana dashboard via curl"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-1.jpg"
description: "Grafana dashboard via curl"

tags: ['kubernetes', 'grafana', 'dashboard', 'curl']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

* do not forget to add "id: null"
* encapsulate to {"dashboard": ...}

```
curl -L \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-X POST \
-uadmin \
--data @/tmp/path/dashboards/dashboard.json \
http://hostname/grafana/api/dashboards/db

```
