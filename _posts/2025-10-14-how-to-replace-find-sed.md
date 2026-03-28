---
title: "How to replace text in lots of file via sed and find"
date: 2024-02-21T15:00:30+0100
lastmod: 2024-02-21T15:00:30+0100
draft: false
description: "How to use find and sed together to perform bulk text replacement across multiple Markdown files."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['sed', 'bash']
categories: ["Linux"]
---


I have recently decided to change the way how my code blocks look like at this blog. This was rather straightforward
change. I needed to exchange "```bash" to "```".

Here is an easy way how this can be achieved via `find` and `sed`. The `find` command locates all Markdown files, and `sed -i` performs an in-place replacement. On macOS, `sed -i ''` requires the empty string argument for the backup extension.

```bash
find content/english -type f -name '*.md' -exec sed -i '' -e 's|\`\`\`bash|\`\`\`|g' {} +
'
```
