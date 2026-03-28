---
title: "How to use magic regexp to replace in vim"
date: 2026-01-19T11:57:07:+0100
lastmod: 2026-01-19T11:57:07:+0100
draft: false
description: "How to use Vim magic regex to transform key-value pairs by lowercasing the key and wrapping it in a variable substitution syntax."
image: "https://i.ytimg.com/vi/YUw1xk82980/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBSJXX-TBEA6uAZg8hLGFgOYk32_g"
author: "Jan Toth"
tags: ["sed", "magic", "regexp", "vim"]
categories: ["Linux"]
---

I have an input string and I would like to take the first column and transform it so that the value behind the `=` sign becomes
the same as the key but lowercased and encapsulated in `${}`.

The Vim substitution command below uses `\v` (very magic mode) to capture the key name with `(\S+)`, then uses `\L` to lowercase the captured group and `\E` to end the case conversion. This is applied to a visual selection with `'<,'>`.

```bash
vim
...
CLIENT_ID = "helloo-id"
TENANT_ID = "helloo-tenant"
CLIENT_SECRET = "helloo-client"
...

:'<,'>s/\v(\S+)\s\=\s(\S+)/\1 = "${\L\1\E}"/

```

Result:

```text
CLIENT_ID = "${client_id}"
TENANT_ID = "${tenant_id}"
CLIENT_SECRET = "${client_secret}"
```
