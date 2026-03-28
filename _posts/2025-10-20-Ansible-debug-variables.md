---
title: "Ansible debug variables"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=420&fit=crop"
description: "How to use the Ansible debug module to inspect all available variables, including environment, group names, groups, and host variables."

tags: ['ansible', 'debug', 'variables']
categories: ["DevOps"]
---

The following Ansible task prints out all available variable categories in a single debug output. This is helpful when troubleshooting playbooks or exploring what data is available at runtime. It collects module variables, environment variables, group names, groups, and host variables and formats them as JSON.

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
