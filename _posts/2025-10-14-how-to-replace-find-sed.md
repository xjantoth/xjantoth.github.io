---
title: "How to replace text in lots of file via sed and find"
date: 2024-02-21T15:00:30+0100
lastmod: 2024-02-21T15:00:30+0100
draft: false
description: "How to replace text in lots of file via sed and find"
image: "assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags:
  - sed
  - find
  - bash
  - replace
---


I have recently decided to change the way how my code blocks look like at this blog. This was rather straightforward
change. I needed to exchange "```bash" to "```".

Here is an easy way how this can be achieved via `find` and `sed`.

```
find content/english -type f -name '*.md' -exec sed -i '' -e 's|\`\`\`bash|\`\`\`|g' {} +
'
```
