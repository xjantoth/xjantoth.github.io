---
title: "Create vim function to generate postman tests"
date: "2021-12-31T16:18:38+0100"
lastmod: "2021-12-31T16:18:38+0100"
draft: false
author: "Jan Toth"
description: "Create vim function to generate postman tests — practical walkthrough with examples."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"

tags: ['vim', 'postman', 'tests']
categories: ["Linux"]
---

This Vim function generates a JSON array of Postman test cases by iterating over a list of field names and test values. It creates every combination of name and value, producing objects with query parameters, expected HTTP response codes, and descriptions. This is useful for quickly scaffolding negative/boundary tests for API endpoints.

```vim
function! CreateTest()
  let a = 0
  let names = ['name', 'vlan_id', 'subnet', 'mask', 'name_network', 'description']
  let values = ['"*"', 'true', '""', '"some_string"', '0', '-1', '100000', '3.543']

  put='['

  for n in names
    for v in values
      let a +=1

      if matchstr(v, '""') == '""'
        let _v = substitute(v,'"\+', '', 'g')
      elseif matchstr(v, '*') == '*'
        let _v = substitute(v,'"\+', '', 'g')
      elseif matchstr(v, '"some_string"') == '"some_string"'
        let _v = substitute(v,'"\+', '', 'g')
      else
        let _v = v
      endif

      put='{\"_query_key\": \"'.n.'\",
            \ \"_query_value\": '.v.',
            \ \"_response\": 200,
            \ \"_description\": \"Invalid search string for '.n.' with value of: '._v.'\",
            \ \"_reason\": \"\",
            \ \"_iteration\": '.a.'}, '
    endfor
  endfor

  put=']'

endfunction
```
