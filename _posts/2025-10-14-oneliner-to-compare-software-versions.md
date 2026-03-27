---
title: Oneliner to compare software versions
date: 2024-03-04T14:41:24+0100
lastmod: 2024-03-04T14:41:24+0100
draft: false
description: "Oneliner to compare software versions — practical walkthrough with examples."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'devopsinuse']
categories: ["Linux"]
---

```bash
export _tags=$(git tag --list  | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+')
export _current=$(curl -s  https://api.github.com/repos/hashicorp/vault/releases | \
jq -r '[.[] | select(.prerelease != true) | .name ] | first' | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+')

[[ $_tags =~ $_current ]] && echo "match" || echo "no match"

```

## Links:

202403041403
