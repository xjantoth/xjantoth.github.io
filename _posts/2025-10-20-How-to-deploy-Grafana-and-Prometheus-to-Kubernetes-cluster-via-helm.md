---
title: "How to deploy Grafana and Prometheus to Kubernetes cluster via helm"
date: "2021-12-30T16:09:28+0100"
lastmod: "2021-12-30T16:09:28+0100"
draft: false
author: "Jan Toth"
description: "Kubernetes cluster (home)"
image: "/assets/images/blog/raspberrypi/raspberrypi.png"

tags: ["raspberry", "grafana", "prometheus", "helm", "deployment"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

**Deploy K3S at Raspberry Pi 4''

```
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644 --tls-san 192.168.0.241 raspberry4-k3s
```

**Setup /etc/hosts at your laptop (ecause of Ingress)''

```
cat /etc/hosts
##
# Host Database
#
...
192.168.0.241 raspberrypi
...


```


**Deploy Grafana''

```
helm upgrade --install grafana grafana/grafana \
--set ingress.enabled=true \
--set "ingress.hosts[0]=raspberrypi" \
--set ingress.path=/grafana \
--set grafana\\.ini.server.root_url="%(protocol)s://%(domain)s/grafana" \
--set grafana\\.ini.server.serve_from_sub_path=true \
--set "datasources.datasources\\.yaml.datasources[0].name=PromethusRaspberryPi" \
--set "datasources.datasources\\.yaml.datasources[0].type=prometheus" \
--set "datasources.datasources\\.yaml.datasources[0].url=http://prometheus-server/prometheus" \
--set dashboards.default.monitoring.gnetId=15120 \
--set dashboards.default.monitoring.revision=3 \
--set dashboards.default.monitoring.datasource=PromethusRaspberryPi \
--set "dashboardProviders.dashboardproviders\\.yaml.providers[0].name=default" \
--set "dashboardProviders.dashboardproviders\\.yaml.providers[0].orgId=1" \
--set "dashboardProviders.dashboardproviders\\.yaml.providers[0].folder=default" \
--set "dashboardProviders.dashboardproviders\\.yaml.apiVersion=1" \
--set "dashboardProviders.dashboardproviders\\.yaml.providers[0].type=file" \
--set "dashboardProviders.dashboardproviders\\.yaml.providers[0].editable=true" \
--set "dashboardProviders.dashboardproviders\\.yaml.providers[0].disableDeletion=true" \
--set "dashboardProviders.dashboardproviders\\.yaml.providers[0].options.path=/var/lib/grafana/dashboards" \
--set persistence.enabled=true \
--set persistence.type=pvc \
--set persistence.size=1Gi \
--set persistence.storageClassName=local-path

```


**Deploy Prometheus''

```
helm upgrade --install prometheus prometheus-community/prometheus \
--set alertmanager.enabled=false \
--set kubeStateMetrics.enabled=false \
--set pushgateway.enabled=false \
--set nodeExporterenabled=false \
--set server.ingress.enabled=true \
--set "server.ingress.hosts[0]=raspberrypi" \
--set server.ingress.path=/prometheus \
--set server.prefixURL=/prometheus \
--set "server.extraFlags[0]=web.external-url=/prometheus" \
--set server.persistentVolume.enabled=true \
--set server.persistentVolume.storageClass=local-path \
--set server.persistentVolume.size=2Gi
```
