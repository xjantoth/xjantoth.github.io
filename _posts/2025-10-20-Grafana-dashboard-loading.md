---
title: "Grafana dashboard loading"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Using Helm to render and inspect Grafana dashboard sidecar configuration templates for Kubernetes deployments."

tags: ['kubernetes', 'grafana', 'dashboard', 'helm']
categories: ["Kubernetes"]
---

Use `helm template` with the `--show-only` flag to render specific templates from the Grafana Helm chart. This is useful for inspecting the configmap dashboard provider and deployment manifests when sidecar dashboard loading is enabled across all namespaces.

```bash
helm repo add grafana https://grafana.github.io/helm-charts

helm template \
--show-only templates/configmap-dashboard-provider.yaml  \
--show-only templates/deployment.yaml  \
--set sidecar.dashboards.enabled=true  \
--set sidecar.dashboards.searchNamespace=ALL  \
grafana/grafana
```
