---
title: "Connecting to PostgreSQL via Cloud SQL Proxy"
date: "2022-01-06T15:00:26+0100"
lastmod: "2022-01-06T15:00:26+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/gcp-1.jpg"
description: "Connecting to PostgreSQL via Cloud SQL Proxy"

tags: ['connecting', 'postgresql', 'cloud', 'sql', 'proxy']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

**Download a postgresql cloud sql proxy binary''

https://cloud.google.com/sql/docs/postgres/connect-admin-proxy?authuser=1&_ga=2.119700096.-903944264.1624478760


```
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
chmod +x cloud_sql_proxy
```


**Open this tunnel in one terminal window''

```
GOOGLE_APPLICATION_CREDENTIALS=/home/jantoth/.google-cloud-keys/wadzpay-dev-cdb0bf1613d2.json

./cloud_sql_proxy  -credential_file=$GOOGLE_APPLICATION_CREDENTIALS -instances=wadzpay-dev:europe-west3:wadzpay-dev-eu-tf=tcp:0.0.0.0:5432

```

**Connect to SQL instance (with private IP only) from your local''

```
psql -h 127.0.0.1 --username=postgres --port=5432 --dbname=postgres
```
**New Firewall rule (default allow) is necessary If having a dedicated VPC''

```
gcloud compute --project=wadzpay-dev firewall-rules create wadzpat-dev-private-allow-internal --direction=INGRESS --priority=65535 --network=wadzpay-dev-private --action=ALLOW --rules=tcp:0-65535,udp:0-65535,icmp --source-ranges=10.128.0.0/9
```
