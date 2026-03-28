---
title: "PostgreSQL RDS AWS"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Connecting to an AWS RDS PostgreSQL instance directly and from within a Kubernetes pod using psql."

tags: ['kubernetes', 'postgresql', 'rds', 'aws']
categories: ["Kubernetes"]
---

The first command connects to an RDS PostgreSQL instance from your local machine using the `psql` client. The second command executes a SQL statement from inside a Kubernetes pod, which is useful when your RDS instance is not publicly accessible and you need to reach it through a pod running in the same VPC.

```bash
psql -h mldb-postgres.cgpyiy4kedtv.us-west-2.rds.amazonaws.com -U postgres -d mldb

kubectl exec pod-demo-0 -it -- \
sh -c "echo 'DROP DATABASE fgh;' | PGPASSWORD=$PGPASSWORD /usr/bin/psql -h 127.0.0.1 -U postgres"
```
