---
title: "Generate SSH kyes for websupport gitlab"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/ssh-1.png"
description: "Generate SSH kyes for websupport gitlab"

tags: ["ssh", "genrerate", "keys", "gitlab", "ssh config"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
ssh-keygen -t rsa -b 4096 -f ~/.ssh/websupport-ssh -C "toth.janci@gmail.com"

git remote add sshorigin git@gitlab.websupport.sk:linuxinuse/arch-dotfiles.git
git add -f <some-file>
git commit -m "Adding some file: <some-file>"
git push sshorigin master

```

Please setup ''~/.ssh/config'' file

```
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
