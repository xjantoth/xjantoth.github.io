---
title: Check permissions for users and service account in GCP via gcloud
date: 2024-07-19T14:15:27+0200
lastmod: 2024-07-19T14:15:27+0200
draft: false
description: Check permissions for users and service account in GCP via gcloud
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags:
  - bash
  - devopsinuse
---


```bash
[arch:tmp ] gcloud projects get-iam-policy <project-name>  \
--flatten="bindings[].members" \
--format='table(bindings.role)' \
--filter="bindings.members:usrname@domain.net"
ROLE
roles/iam.serviceAccountUser
roles/owner
roles/serviceusage.serviceUsageAdmin

```

## Links:

202407191407
