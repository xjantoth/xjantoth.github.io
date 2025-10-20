---
title: "PostgreSQL RDS AWS"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-1.jpg"
description: "PostgreSQL RDS AWS"

tags: ["kubernetes", "postgresql", "rds", "aws"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
psql -h mldb-postgres.cgpyiy4kedtv.us-west-2.rds.amazonaws.com -U postgres -d mldb

kubectl exec pod-demo-0 -it -- \
sh -c "echo 'DROP DATABASE fgh;' | PGPASSWORD=$PGPASSWORD /usr/bin/psql -h 127.0.0.1 -U postgres"
```
