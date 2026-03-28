---
title: "Go variables"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Understanding Go variable declarations, type conversions between int and float32, and converting integers to strings with strconv."

tags: ['go', 'variables']
categories: ["Go"]
---

This example shows how to declare variables in Go using both the `var` keyword and the short declaration operator `:=`. It also demonstrates package-level variable blocks, type conversion between `int` and `float32`, and converting an integer to a string using `strconv.Itoa`. Note that in Go, declared but unused variables cause a compile error.

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
