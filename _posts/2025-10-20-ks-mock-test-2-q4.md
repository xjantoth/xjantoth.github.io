---
title: "CKS Mock test 2 - Q4"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "CKS Mock test 2 - Q4"

tags: ['cks', 'mock', 'test', 'q4']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

**4. A pod in the sahara namespace has generated alerts that a shell was opened inside the container.


Change the format of the output so that it looks like below:
ALERT timestamp of the event without nanoseconds,User ID,the container id,the container image repository
Make sure to update the rule in such a way that the changes will persists across Falco updates.
You can refer the falco documentation Here
**

```
vim +/"A shell was spawned in a container with an attached" /etc/falco/falco_rules.yaml
```


```
cat  /etc/falco/falco_rules.local.yaml
#
# Copyright (C) 2019 The Falco Authors.
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

####################
# Your custom rules!
####################

# Add new rules, like this one
# - rule: The program "sudo" is run in a container
#   desc: An event will trigger every time you run sudo in a container
#   condition: evt.type = execve and evt.dir=< and container.id != host and proc.name = sudo
#   output: "Sudo run in container (user=%user.name %container.info parent=%proc.pname cmdline=%proc.cmdline)"
#   priority: ERROR
#   tags: [users, container]

# Or override/append to any rule, macro, or list from the Default Rules
- rule: Terminal shell in container
  desc: A shell was used as the entrypoint/exec point into a container with an attached terminal.
  condition: >
    spawned_process and container
    and shell_procs and proc.tty != 0
    and container_entrypoint
    and not user_expected_terminal_shell_in_container_conditions
  output: >
    timestamp=%evt.time.s user_loginuid=%user.loginuid container_id=%container.id image=%container.image.repository
  priority: ALERT
  tags: [container, shell, mitre_execution]

```
