---
title: "Backend helm chart running on Kubernetes"
date: "2021-12-30T16:09:28+0100"
lastmod: "2021-12-30T16:09:28+0100"
draft: false
author: "Jan Toth"
description: "backend helm chart"
image: "/assets/images/blog/kubernetes-1.jpg"

tags: ["raspberry", "helm", "backend", "k8s"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```bash

## Do some fancy replacements
```bash
sed -E \
-e 's/^(description:).*/\1 Raspberry Pi Backend helm chart/' \
-e 's/^(appVersion:).*/\1 0.0.1 /' \
-e '$a  \\ndependencies: \n- name: postgresql \n  version: "9.8.3" \n  repository: "https://charts.bitnami.com/bitnami" \n' \
-i backend/Chart.yaml
```

## Add helm chart registry

```bash
helm repo list
helm repo add bitnami https://charts.bitnami.com/bitnami
helm dependency update backend

sed -E \
-e 's/^(.*paths:).*/\1 ["\/api"]/' \
-e '/^ingress.*/,/^\s*tls:.*/s/^(.*-\shost: )(.*)/\1 raspberrypi--weather-monitoring/' \
-e '/^.*pullPolicy:.*/a \ \ containerPort: 8000' \
-e '/^.*pullPolicy:.*/a \ \ # Database connection settings:' \
-e '/^.*pullPolicy:.*/a \ \ env:' \
-e '/^.*pullPolicy:.*/a \ \ \ \ secret:' \
-e '/^.*pullPolicy:.*/a \ \ \ \ \ \ PSQL_DB_USER: "micro"' \
-e '/^.*pullPolicy:.*/a \ \ \ \ \ \ PSQL_DB_PASS: "password"' \
-e '/^.*pullPolicy:.*/a \ \ \ \ \ \ PSQL_DB_NAME: "microservice"' \
-e '/^.*pullPolicy:.*/a \ \ \ \ \ \ PSQL_DB_ADDRESS: "backend-postgresql"' \
-e '/^.*pullPolicy:.*/a \ \ \ \ \ \ PSQL_DB_PORT: "5432"' \
-e '$a \\nlivenessProbe: \/api\/health' \
-e '$a \\nreadinessProbe: \/api\/health' \
-e 's/^(.*repository:).*/\1 jantoth\/weather-backend/' \
-i backend/values.yaml
```


## Create backend values.yaml file

```bash
cat <<'EOF' >>backend/values.yaml

postgresql:
  image:
    registry: docker.io
    repository: bitnami/postgresql
    tag: latest
    debug: true

  global:
    postgresql:
      postgresqlUsername: postgres
      postgresqlPassword: password

  persistence:
    enabled: false

  pgHbaConfiguration: |
    local all all trust
    host all all localhost trust
    host microservice micro 10.42.0.0/16 password

  initdbScripts:
    db-init.sql: |
      CREATE DATABASE microservice;
      CREATE USER micro WITH ENCRYPTED PASSWORD 'password';
      GRANT ALL PRIVILEGES ON DATABASE microservice TO micro;
      ALTER DATABASE microservice OWNER TO micro;

EOF
```

## Set targetPort 

```bash
{% raw %}
sed -E \
-e 's/^(.*targetPort:).*/\1 {{ .Values.image.containerPort | default 80 }}/' \
-i backend/templates/service.yaml
{% endraw %}
```



## Setup "livenessProbe" and "readinessProbe" in backend/templates/deployment.yaml

```bash
{% raw %}
sed -E \
-e '/^\s*livenessProbe:.*/,/^\s*port:.*/s/^(.*port:)(.*)/\1 {{ .Values.image.containerPort | default "http" }}/' \
-e '/^\s*readinessProbe:.*/,/^\s*port:.*/s/^(.*port:)(.*)/\1 {{ .Values.image.containerPort | default "http" }}/' \
-e '/^\s*livenessProbe:.*/,/^\s*port:.*/s/^(.*path:)(.*)/\1 {{ .Values.livenessProbe | default "\/" }}/' \
-e '/^\s*readinessProbe:.*/,/^\s*port:.*/s/^(.*path:)(.*)/\1 {{ .Values.readinessProbe | default "\/" }}/' \
-e 's/^(.*containerPort:).*/\1 {{ .Values.image.containerPort }}/' \
-e '/^.*image:.*/a \ \ \ \ \ \ \ \ \ \ env:' \
-e '/^.*image:.*/a \ \ \ \ \ \ \ \ \ \ {{- include "helpers.list-env-variables" . | indent 10 }}' \
-i backend/templates/deployment.yaml
```
{% endraw %}

## Creating file: "backend/templates/secret.yaml"

```bash
cat <<'EOF' >>backend/templates/secret.yaml
{% raw %}
apiVersion: v1
kind: Secret
metadata:
  name: database-conection
type: Opaque
data:
  {{- range $key, $val := .Values.image.env.secret }}
  {{ $key }}: {{ $val | b64enc }}
  {{- end}}
{% endraw %}
EOF
```


## Helper tpl

```bash

{% raw %}
cat <<'EOF' >>backend/templates/_helpers.tpl

{{/*
Create the looper to define secret mounts as ENV variables
*/}}

{{- define "helpers.list-env-variables"}}
{{- range $key, $val := .Values.image.env.secret }}
- name: {{ $key }}
  valueFrom:
    secretKeyRef:
      name: database-conection
      key: {{ $key }}
{{- end}}
{{- end}}
EOF
{% endraw %}
```
