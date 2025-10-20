---
title: "Create more configMaps via Go templating"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-1.jpg"
description: "Create more configMaps via Go templating"

tags: ['kubernetes', 'go', 'templating', 'configmap']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

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
