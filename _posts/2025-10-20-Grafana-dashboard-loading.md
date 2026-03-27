---
title: "Grafana dashboard loading"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Kubernetes: Grafana dashboard loading — configuration and practical examples."

tags: ['kubernetes', 'grafana', 'dashboard', 'helm']
categories: ["Kubernetes"]
---

```
helm repo add grafana https://grafana.github.io/helm-charts

helm template \
--show-only templates/configmap-dashboard-provider.yaml  \
--show-only templates/deployment.yaml  \
--set sidecar.dashboards.enabled=true  \
--set sidecar.dashboards.searchNamespace=ALL  \
grafana/grafana
```
