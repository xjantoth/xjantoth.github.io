---
title: "Create more configMaps via Go templating"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Go programming: Create more configMaps via Go templating with working code examples."

tags: ['kubernetes', 'go', 'templating', 'configmap']
categories: ["Kubernetes"]
---

The following Helm template snippet uses Go templating to iterate over all JSON files in a `dashboards/` directory and generate a separate Kubernetes ConfigMap for each one. This is commonly used to provision Grafana dashboards automatically via sidecar.

```go
{% raw %}
{{ range $path, $_ :=  .Files.Glob  "dashboards/*.json" }}
{{- $dashboardName :=  trimSuffix ".json"  $path | base | replace "_" "-" | lower -}}
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: "{{ template "grafana.fullname" $ }}-{{ $dashboardName }}"
  namespace: {{ template "grafana.namespace" $ }}
  labels:
    {{- include "grafana.labels" $ | nindent 4 }}
    grafana_dashboard: "1"
data:
  {{ $dashboardName }}.json: |-
{{ $.Files.Get $path | indent 4}}
{{ end }}
{% endraw %}

```
