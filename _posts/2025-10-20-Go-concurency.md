---
title: "Go concurency"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Go programming: Go concurency with working code examples."

tags: ['go', 'concurency']
categories: ["Go"]
---

```go
// package main

// import (
// 	"fmt"
// 	// "strconv"
// 	// "math"
// 	// "reflect"
// 	// "net/http"
// 	// "log"

// )

// // define interface
// type Writer interface {
// 	Write([]byte) (int, error)
// }

// type ConsoleWriter struct {}

// func (cw ConsoleWriter) Write(data []byte) (int, error) {
// 	n, err := fmt.Printf("Converts bytes to string: %v\n", string(data))
// 	return n, err
// }

// func main()  {
// 	var w Writer = ConsoleWriter{}
// 	w.Write([]byte("101010100001"))
// }

package main

import (
	"fmt"
	"time"
)

func sayHello()  {
	fmt.Printf("Say hello\n")
}

func main()  {
	go sayHello()
	time.Sleep(100 * time.Millisecond)

// bad approach
var msg string = "hello"
go func (i string)  {
	fmt.Printf("%v\n", i)
}(msg)
msg = "Goodbye"
time.Sleep(100 * time.Millisecond)
}

```
