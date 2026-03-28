---
title: "How to count numbers from pdf"
date: 2022-02-09T13:17:15+0100
lastmod: 2022-02-09T13:17:15+0100
draft: false
description: "It is possible to extract pdf text and get some valuable information out of it."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['pdf']
categories: ["Linux"]
---


It is possible to extract PDF text and get some valuable information out of it.

This pipeline extracts USD amounts from multiple PDF files, sums them up, and prints the total. It uses `pdftotext` to convert PDFs to text, `grep` to find lines matching a USD pattern, `sed` to normalize the decimal separator, and `awk` to compute the sum. You need `pdftotext` (from the `poppler` package) installed.

```bash

for i in $(ls *.pdf); do \
pdftotext $i - | grep -E '^\+.*(USD)$'; done \
| grep -Eo '[0-9]+,[0-9]+' --color \
| sed 's/,/./g' \
| awk '{s+=$1}END{print s}'

```
