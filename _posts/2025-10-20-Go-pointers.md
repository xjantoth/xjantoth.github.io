---
title: "Go pointers"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Go programming: Go pointers with working code examples."

tags: ['go', 'pointers']
categories: ["Go"]
---

```go
package main

import (
	"fmt"
	// "strconv"
	// "math"
	// "reflect"
	// "net/http"
	// "log"

)

func simple()  {
	a := 42
	// b will be a brand new variable with it's place in memory
	b := a
	fmt.Printf("a: %v, b: %v\n", a, b)
	a = 27
	fmt.Printf("a: %v, b: %v\n", a, b)

}

func withPointer()  {
	var a int = 42
	var b *int = &a
	fmt.Printf("a: %v, b(memory location): %v, dereferencing: %v\n", a, b, *b)
	a = 27
	fmt.Printf("a: %v, b(memory location): %v, dereferencing: %v\n", a, b, *b)
}

func aritmwithPointer()  {
	a := [3]int{1, 2, 3}
	b := &a[0]
	c := &a[1]

	fmt.Printf("a: %v, b: %v, c: %v\n", a, b, c)
	fmt.Printf("a: %v, b: %v, c: %v\n", a, *b, *c)
	fmt.Printf("a: %v, b: %p, c: %p\n", a, b, c)

	var ms myStruct
	ms = myStruct{foo: 42}

	// var ms *myStruct
	// ms = &myStruct{foo: 42}

	fmt.Println(ms.foo)
}

type myStruct struct {
	foo int
}

func main() {
	// simple()
	// withPointer()
	aritmwithPointer()
}
```
