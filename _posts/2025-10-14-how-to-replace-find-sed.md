---
title: "How to replace text in lots of file via sed and find"
date: 2024-02-21T15:00:30+0100
lastmod: 2024-02-21T15:00:30+0100
draft: false
description: "I have recently decided to change the way how my code blocks look like at this blog. This was rather straightforward change. I needed to exchange \"``bash\" to \"``\"."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['sed', 'bash']
categories: ["Linux"]
---


I have recently decided to change the way how my code blocks look like at this blog. This was rather straightforward
change. I needed to exchange "```bash" to "```".

Here is an easy way how this can be achieved via `find` and `sed`.

```
find content/english -type f -name '*.md' -exec sed -i '' -e 's|\`\`\`bash|\`\`\`|g' {} +
'
```
