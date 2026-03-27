---
title: "Grafana dashboard via curl"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Do not forget to add \"id: null\" encapsulate to {\"dashboard\": ...}."

tags: ['kubernetes', 'grafana', 'dashboard', 'curl']
categories: ["Kubernetes"]
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
