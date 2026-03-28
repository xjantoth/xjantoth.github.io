---
title: "Go pointers"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How pointers work in Go, including the address-of operator, dereferencing, pointer arithmetic with arrays, and pointers to structs."

tags: ['go', 'pointers']
categories: ["Go"]
---

This program demonstrates pointers in Go. It first shows how assigning one variable to another creates a copy (they are independent in memory). Then it introduces the `&` (address-of) operator and `*` (dereference) operator to work with pointers, which allow two variables to reference the same memory location. The final example shows taking pointers to array elements and using pointers with structs.

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
