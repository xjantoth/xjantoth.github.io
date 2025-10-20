---
title: How to pass --url-query to curl
date: 2024-06-10T13:50:44+0200
lastmod: 2024-06-10T13:50:44+0200
draft: false
description: How to pass --url-query to curl
image: https://cdn.shortpixel.ai/spai/q_lossy+ret_img+to_auto/linuxiac.com/wp-content/uploads/2020/07/curl.jpg
author: "Jan Toth"
tags:
  - bash
  - devopsinuse
  - curl
---

This is a nice way how to multiline query parameters when using `curl`


```
curl "https://example.cloud/drms/whatever/rest/deployrequests" \
--url-query "deployFromDate=10.06.2023" \
--url-query "deployToDate=10.06.2024" \
--url-query "showStates=Defined,Locked,Failed,Confirmed,Succeeded" \
-H "Authorization: Bearer ..."   \
-H 'Referer: https://.../history'  \
-H 'Accept: application/json, text/plain, */*'  | jq

```

