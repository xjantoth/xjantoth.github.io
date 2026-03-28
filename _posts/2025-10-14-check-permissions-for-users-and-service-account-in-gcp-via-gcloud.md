---
title: Check permissions for users and service account in GCP via gcloud
date: 2024-07-19T14:15:27+0200
lastmod: 2024-07-19T14:15:27+0200
draft: false
description: "Check permissions for users and service account in GCP via gcloud — practical walkthrough with examples."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'devopsinuse']
categories: ["Linux"]
---

The following `gcloud` command checks what IAM roles are assigned to a specific user or service account within a GCP project. It flattens the IAM policy bindings and filters by the member's email address, which is useful for auditing permissions.

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

