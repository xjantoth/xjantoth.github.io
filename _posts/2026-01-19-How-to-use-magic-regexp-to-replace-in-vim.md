---
title: "How to use magic regexp to replace in vim"
date: 2026-01-19T11:57:07:+0100
lastmod: 2026-01-19T11:57:07:+0100
draft: false
description: "How to use magic regexp to replace in vim"
image: "https://i.ytimg.com/vi/YUw1xk82980/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBSJXX-TBEA6uAZg8hLGFgOYk32_g"
author: "Jan Toth"
tags: ["sed", "magic", "regexp", "vim"]
---

I have an input string and I would like to take first column and transfer it in a way that the value behind = sign would be
the same as the key but lowercased and encapsulated in "${}".



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

```
CLIENT_ID = "${client_id}"
TENANT_ID = "${tenant_id}"
CLIENT_SECRET = "${client_secret}"

```
