---
title: "Connecting to PostgreSQL via Cloud SQL Proxy"
date: "2022-01-06T15:00:26+0100"
lastmod: "2022-01-06T15:00:26+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to connect to a Google Cloud SQL PostgreSQL instance using the Cloud SQL Proxy, including downloading the binary, establishing the tunnel, and configuring firewall rules."

tags: ['connecting', 'postgresql', 'cloud', 'sql', 'proxy']
categories: ["DevOps"]
---

**Download the Cloud SQL Proxy binary**

Reference: https://cloud.google.com/sql/docs/postgres/connect-admin-proxy

Download the Cloud SQL Proxy binary and make it executable. This proxy creates a secure tunnel to your Cloud SQL instance.

```bash
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
chmod +x cloud_sql_proxy
```


**Open this tunnel in one terminal window**

Start the Cloud SQL Proxy, pointing it to your service account credentials and the target Cloud SQL instance. The proxy will listen on localhost port 5432.

```bash
GOOGLE_APPLICATION_CREDENTIALS=/home/jantoth/.google-cloud-keys/wadzpay-dev-cdb0bf1613d2.json

./cloud_sql_proxy  -credential_file=$GOOGLE_APPLICATION_CREDENTIALS -instances=wadzpay-dev:europe-west3:wadzpay-dev-eu-tf=tcp:0.0.0.0:5432

```

**Connect to the SQL instance (with private IP only) from your local machine**

With the proxy running, connect to the PostgreSQL instance through the local tunnel using `psql`.

```bash
psql -h 127.0.0.1 --username=postgres --port=5432 --dbname=postgres
```
**New firewall rule (default allow) is necessary if using a dedicated VPC**

If your Cloud SQL instance is in a private VPC, you need to create a firewall rule that allows internal traffic between resources.

```bash
gcloud compute --project=wadzpay-dev firewall-rules create wadzpat-dev-private-allow-internal --direction=INGRESS --priority=65535 --network=wadzpay-dev-private --action=ALLOW --rules=tcp:0-65535,udp:0-65535,icmp --source-ranges=10.128.0.0/9
```
