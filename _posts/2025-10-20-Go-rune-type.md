---
title: "Go rune type"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Understanding Go's rune type, which is an alias for int32 used to represent Unicode code points."

tags: ['go', 'rune', 'type']
categories: ["Go"]
---

This snippet demonstrates Go's rune type, which is an alias for `int32`. A rune represents a Unicode code point. The example also shows how to convert a string to a byte slice using `[]byte()`. Note that strings in Go must use double quotes, while single quotes are reserved for rune literals.

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
