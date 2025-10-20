---
title: How to assemble project name based on yaml content using jq
date: 2024-06-28T10:39:00+0200
lastmod: 2024-06-28T10:39:00+0200
draft: false
description: How to assemble project name based on yaml content using jq
image: https://miro.medium.com/1*Kmn2vLqmIGiaUdc2-oaNRw.png
author: "Jan Toth"
tags:
  - bash
  - devopsinuse
  - jq
---


If you have multiple files without proper names, you can generate project names based on the values in the YAML files.
Here's a solution that uses yq and jq to extract and format these names.


```
solution(){

  for i in $(find . -type f -name "RI*.yaml" | xargs -I % sh -c 'echo %'); do
    FN=${i##*/};
    name=$(yq -o json eval $i | jq -r '[(.solution_name),(.use_case // ""),(if .suffix then .suffix|tostring else "0" end)]| map(select(length > 0)) | join("-")');
    oo=${${i##*organization/}%%/*};
    if [[ "$oo" == *"dev"* ]]; then org="deaut"; else org="eaut"; fi;

    project_name="$org-${${i##*environments/}%%/*}-$name";
    echo "${i} ${project_name}"

  done > /tmp/solutions.txt

  export BAT_THEME='gruvbox-dark'
  RG_PREFIX="rg --column --line-number --no-heading --color=always --smart-case < /tmp/solutions.txt"

  INITIAL_QUERY="${*:-}"
  : | fzf --ansi --disabled --query "$INITIAL_QUERY" \
      --bind "start:reload:$RG_PREFIX {q}" \
      --bind "change:reload:sleep 0.1; $RG_PREFIX {q} || true" \
      --bind "alt-enter:unbind(change,alt-enter)+change-prompt(2. fzf> )+enable-search+clear-query" \
      --color "hl:-1:underline,hl+:-1:underline:reverse" \
      --prompt '1. ripgrep> ' \
      --delimiter ': ' \
      --preview 'bat --color=always -l yaml $(echo {1} | grep -oE "\.\/.*\s")' \
      --preview-window 'up,80%,border-bottom,+{2}+3/3,~3' \
      --bind 'enter:become(lvim $(echo {1} | grep -oE "\.\/.*\s"); echo $(echo {1} | grep -oE "\.\/.*\s"); echo $(echo {1} | grep -oE "\.\/.*\s") | pbcopy)'

}

```

## Explanation
- Finding YAML Files: The script searches for YAML files with names starting with "RI" in the current directory and subdirectories.
- Extracting Values: It extracts values from these YAML files using yq and jq. It forms a name from solution_name, use_case, and suffix.
- Organizing Names: Based on whether the file is for a development environment or not, it sets a prefix (deaut or eaut) and constructs the project name.
- Storing Results: The results are saved in /tmp/solutions.txt.
- Interactive Search: The script then uses fzf for interactive search, displaying the YAML content with syntax highlighting.

- This method ensures consistent and meaningful project names derived directly from the YAML file content.


