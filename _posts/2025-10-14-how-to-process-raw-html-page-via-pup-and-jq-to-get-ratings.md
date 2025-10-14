---
title: How to process raw html page via pup and jq to get ratings
date: 2024-07-18T12:29:43+0200
lastmod: 2024-07-18T12:29:43+0200
draft: false
description: How to process raw html page via pup and jq to get ratings
image: "images/blog/linux-1.jpg"
author: "Jan Toth"
tags:
  - bash
  - devopsinuse
  - jq
  - pup

---


The friend of mine wrote Bash script that parses raw HTML page using grep and loops to find images with rating higher
than some number.

Here is in my opinion a simplified version of that script using `jq` and `pup`.

It turnes out that `pup` binary is preinstalled at my Mac and I use `jq` pretty much everyday.
`pup` binary converts raw HTML to `json` format that can be later on relatively easy used to parse "likes" and respective URLs.

```bash
#!/bin/bash


export RATING=30
wget https://www.rouming.cz -O - | \
  pup 'div.wrapper json{}' | \
  jq -r '.[] | .children[0].children[0].children[0].children
  | .[] | {
    likes: .children[3].children[0].text|tonumber,
    dislikes: .children[5].children[0].text|tonumber,
    url: .children[6].children[0].href,
    rating: ((.children[3].children[0].text|tonumber) - (.children[5].children[0].text|tonumber))|tonumber
  }
  | select(.rating >= '$RATING')' \
  | jq -sr '. |=sort_by(.rating) | .[] | .url'


```

## Links:

202407181207
