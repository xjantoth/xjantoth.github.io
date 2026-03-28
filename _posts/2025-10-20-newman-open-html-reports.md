---
title: "Newman Open HTML Reports"
date: "2022-01-07T11:20:36+0100"
lastmod: "2022-01-07T11:20:36+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Quick one-liner to open the most recently generated Newman HTML report in your default browser on macOS."

tags: ['newman', 'open', 'html', 'reports']
categories: ["DevOps"]
---

This command finds the most recently created file in the `newman/` directory (sorted by modification time), resolves its full path using `greadlink`, and opens it in your default browser. This is handy after running a Newman test suite with the `htmlextra` reporter to quickly view results.

```bash
open "$(greadlink -f  "$(ls -tr newman/* | tail -n 1 )")"
```
