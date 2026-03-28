---
title: "Go methods"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to define and use methods on structs in Go, demonstrated with a greeter struct that has a greet method."

tags: ['go', 'methods']
categories: ["Go"]
---

This program demonstrates methods in Go. Unlike traditional OOP languages, Go attaches methods to types using a receiver parameter. Here, the `greeter` struct has a `greet()` method with a value receiver `(g greeter)`. When called, the method has access to the struct's fields and can format a greeting message.

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


type greeter struct {
	greeting string
	name string
}

func (g greeter) greet() {
	fmt.Printf("%v: %v\n", g.greeting, g.name)
}

func main()  {
	a := greeter{
		greeting: "Hello",
		name: "Gooers!",
	}

	a.greet()
}



```
