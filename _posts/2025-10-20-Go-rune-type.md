---
title: "Go rune type"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go rune type"

tags: ['go', 'rune', 'type']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
func arrays()  {
	// !!! if declating string -> use double quotes ""
	s := "this is a string"
	b := []byte(s)
	fmt.Printf("%v, %T\n", b, b)

	// !!! rune <- this is a type and it is represented as int32
	// "rune" is a type alias for "int32"
	r := 'a'
	var x rune = 'a'

	fmt.Printf("%v, %T", r, r)
	fmt.Printf("%v, %T", x, x)
}
```
