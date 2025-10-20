---
title: "How to count numbers from pdf"
date: 2022-02-09T13:17:15+0100
lastmod: 2022-02-09T13:17:15+0100
draft: false
description: "How to count numbers from pdf"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ["pdf"]
---


It is possible to extract pdf text and get some valuable information out of it.


```bash

for i in $(ls *.pdf); do \
pdftotext $i - | grep -E '^\+.*(USD)$'; done \
| grep -Eo '[0-9]+,[0-9]+' --color \
| sed 's/,/./g' \
| awk '{s+=$1}END{print s}'

```
