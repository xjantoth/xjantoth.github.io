---
title: "How to run n8s on locally on Apple containers Mac"
date: 2025-10-21T11:10:11:+0200
lastmod: 2025-10-21T11:10:11:+0200
draft: false
description: "Apple has recently introduced their own container solution. I have decided to test it and start n8n. This is what the official GitHub n8n instruction says."
image: "https://i.ytimg.com/vi/YUw1xk82980/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBSJXX-TBEA6uAZg8hLGFgOYk32_g"
author: "Jan Toth"
tags: ['mac', 'containers', 'n8s']
categories: ["Docker"]
---

Apple has recently introduced their own container solution. I have decided to test it and start n8n.
This is what the official GitHub n8n instruction says.

```bash
docker volume create n8n_data
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

However, I have decided to test it with the `container` command that I installed on my Mac. The Apple container runtime uses a slightly different CLI, and it does not support the `-v` volume mount flag in the same way as Docker.

```bash
brew install container
container system start

container run -it --rm --name n8n -p 5678:5678  docker.n8n.io/n8nio/n8n

No encryption key found - Auto-generating and saving to: /home/node/.n8n/config
Permissions 0644 for n8n settings file /home/node/.n8n/config are too wide. This is ignored for now, but in the future n8n will attempt to change the permissions automatically. To automatically enforce correct permissions now set N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true (recommended), or turn this check off set N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=false.
Initializing n8n process
n8n ready on ::, port 5678
Migrations in progress, please do NOT stop the process.
Starting migration InitialMigration1588102412422
Finished migration InitialMigration1588102412422
Starting migration WebhookModel1592445003908
...
```

And, what can I say -- it works like a charm!
