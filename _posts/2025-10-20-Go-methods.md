---
title: "Go methods"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Go programming: Go methods with working code examples."

tags: ['go', 'methods']
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
