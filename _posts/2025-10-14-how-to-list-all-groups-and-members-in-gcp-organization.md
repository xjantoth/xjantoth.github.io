---
title: How to list all groups and members in GCP organization
date: 2024-11-14T11:41:11+0100
lastmod: 2024-11-14T11:41:11+0100
draft: false
description: How to list all groups and members in GCP organization
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['bash', 'devopsinuse', 'gcloud', 'gcp']
---

```bash
gcloud identity groups search --labels="cloudidentity.googleapis.com/groups.discussion_forum" --organization="111111111111" --page-size=3000 --format=json > groups.json

for i in $(cat groups.json | jq -r '.[] | .groups | .[] | .groupKey.id' | grep admin); do
  match=$(gcloud identity groups memberships list --group-email=$i --format=json | jq -r '.[] | .preferredMemberKey.id')
  if echo $match | grep -v -q "^sy"; then echo "---\n$i:\n$match"; fi
done
```

