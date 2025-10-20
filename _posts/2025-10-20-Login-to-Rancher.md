---
title: "Login to Rancher"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-1.jpg"
description: "Login to Rancher"

tags: ['kubernetes', 'work', 'login', 'rancher']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
NAME="rancher.web.ui"
RANCHER_URL="https://$NAME:10443"

APITOKEN=$(curl -sk "${RANCHER_URL}/v3-public/localProviders/local?action=login" \
-H "content-type: application/json" \
--data-binary "{\"username\":\"admin\",\"password\":\"admin\"}" 2>/dev/null | jq -r .token 2>/dev/null)

rancher login -t "${APITOKEN}" "${RANCHER_URL}/v3"
```
