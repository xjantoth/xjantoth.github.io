---
title: "Generate SSH keys for Websupport GitLab"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=800&h=420&fit=crop"
description: "How to generate SSH keys and configure ~/.ssh/config for pushing to a Websupport-hosted GitLab repository."

tags: ['ssh', 'genrerate', 'keys', 'gitlab', 'ssh config']
categories: ["CI/CD"]
---

First, generate a new SSH key pair and then add the remote repository using the SSH URL. After that, you can commit and push files to the Websupport GitLab instance over SSH.

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/websupport-ssh -C "toth.janci@gmail.com"

git remote add sshorigin git@gitlab.websupport.sk:linuxinuse/arch-dotfiles.git
git add -f <some-file>
git commit -m "Adding some file: <some-file>"
git push sshorigin master

```

Next, set up the `~/.ssh/config` file so that SSH automatically uses the correct key when connecting to `gitlab.websupport.sk`.

```text
vim ~/.ssh/config

...
# linuxinuse account
Host gitlab.websupport.sk
        HostName gitlab.websupport.sk
        User git
        IdentitiesOnly yes
        IdentityFile ~/.ssh/websupport-ssh
...
:wq!
```
