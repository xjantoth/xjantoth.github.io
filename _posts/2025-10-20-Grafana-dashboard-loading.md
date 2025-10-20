---
title: "Grafana dashboard loading"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-1.jpg"
description: "Grafana dashboard loading"

tags: ['kubernetes', 'grafana', 'dashboard', 'helm']
categories: ["tiddlywiki"]

hiddenFromSearch: false
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
