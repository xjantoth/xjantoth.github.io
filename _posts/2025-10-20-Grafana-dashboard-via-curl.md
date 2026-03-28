---
title: "Grafana dashboard via curl"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "How to import a Grafana dashboard via the HTTP API using curl, including the required JSON structure with id null and the dashboard wrapper."

tags: ['kubernetes', 'grafana', 'dashboard', 'curl']
categories: ["Kubernetes"]
---

* do not forget to add "id: null"
* encapsulate to {"dashboard": ...}

The following `curl` command imports a Grafana dashboard via the HTTP API. The JSON payload must be wrapped in a `{"dashboard": ...}` envelope and the `id` field should be set to `null` to create a new dashboard rather than updating an existing one.

```bash
curl -L \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-X POST \
-uadmin \
--data @/tmp/path/dashboards/dashboard.json \
http://hostname/grafana/api/dashboards/db

```
