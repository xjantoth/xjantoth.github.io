---
title: "Go methods"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go methods"

tags: ['go', 'methods']
categories: ["tiddlywiki"]

hiddenFromSearch: false
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
