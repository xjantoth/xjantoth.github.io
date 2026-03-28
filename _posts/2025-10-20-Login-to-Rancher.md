---
title: "Login to Rancher"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "How to authenticate to a Rancher server via the API and log in using the Rancher CLI."

tags: ['kubernetes', 'login', 'rancher']
categories: ["Kubernetes"]
---

The following script authenticates against the Rancher local provider API to obtain an API token, then uses that token to log in via the Rancher CLI. Replace the URL and credentials with your actual Rancher server details.

```bash
NAME="rancher.web.ui"
RANCHER_URL="https://$NAME:10443"

APITOKEN=$(curl -sk "${RANCHER_URL}/v3-public/localProviders/local?action=login" \
-H "content-type: application/json" \
--data-binary "{\"username\":\"admin\",\"password\":\"admin\"}" 2>/dev/null | jq -r .token 2>/dev/null)

rancher login -t "${APITOKEN}" "${RANCHER_URL}/v3"
```
