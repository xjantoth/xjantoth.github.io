---
title: "Ansible debug variables"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Ansible debug variables"

tags: ["ml"]
categories: ["tiddlywiki", "ansible", "variable"]

hiddenFromSearch: false
---

```yaml
- name: xyz
  vars:
    msg: |
      Module Variables ("vars"):
      --------------------------------
      {% raw %}{{ vars | to_nice_json }}{% endraw %}

      Environment Variables ("environment"):
      --------------------------------
      {% raw %}{{ environment | to_nice_json }}{% endraw %}

      GROUP NAMES Variables ("group_names"):
      --------------------------------
      {% raw %}{{ group_names | to_nice_json }}{% endraw %}

      GROUPS Variables ("groups"):
      --------------------------------
      {% raw %}{{ groups | to_nice_json }}{% endraw %}

      HOST Variables ("hostvars"):
      --------------------------------
      {% raw %}{{ hostvars | to_nice_json }}{% endraw %}

  debug:
    msg: "{% raw %}{{ msg.split('\n') }}{% endraw %}"
  tags: debug_info
```
