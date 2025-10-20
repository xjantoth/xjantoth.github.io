---
title: "Go variables"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go variables"

tags: ['go', 'variables']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
package main

import (
	"fmt"
	"strconv"
)

// if declaring vatiable over here
// you can't use a := 10
var (
	a int = 42
	actorName string = "Elisabeth Salden"
	companion string = "Sarah Elisabeth Salden"
	// example of acronym
	theHTTP string = "https://google.com"
	doctorNumber int = 11
	season int = 10

)

var I int = 30

func main()  {
	// var i int
	var i int = 40
	var j int = 30
	var x float32 = 10

	var g float32
	g = float32(j)
	// if variable is declared and not used -> you will get a compile error
	k := i + j

	var s string
	s = strconv.Itoa(i)


	fmt.Println("Hello from Go!", k)
	fmt.Printf("Hello from Go! %v %T\n", k, k)
	fmt.Printf("Float number! %v %T\n", x, x)
	fmt.Printf("This variable was converted to float32: %v, %T\n", g, g)
	fmt.Printf("Converting int -> string: %s, %T\n", s, s)
}
```
