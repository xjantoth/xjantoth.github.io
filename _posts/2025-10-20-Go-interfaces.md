---
title: "Go interfaces"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to define and implement interfaces in Go, demonstrated with a Shape interface that requires Area and Perimeter methods."

tags: ['go', 'interfaces']
categories: ["Go"]
---

This program demonstrates Go interfaces. A `Shape` interface is defined with `Area()` and `Perimeter()` methods. The `Rect` struct implements both methods, which means it implicitly satisfies the `Shape` interface without any explicit declaration. The example shows how a `Rect` value can be assigned to a `Shape` variable and how methods can be called through both the interface and the concrete type.

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
)

type Shape interface {
	Area() float64
	Perimeter() float64

}

type Rect struct {
	width float64
	hight float64
}

func (r Rect) Area() float64 {
	return r.width * r.hight
}

func (r Rect) Perimeter() float64 {
	return 2 * (r.width + r.hight)
}

func main()  {
	var s Shape = Rect{
		width: 5.0,
		hight: 4.0,
	}

	r := Rect{
		width: 5.0,
		hight: 4.0,
	}

	fmt.Printf("%v\n", s.Perimeter())
	fmt.Printf("%v\n", s.Area())
	fmt.Printf("%T\n", s)

	fmt.Printf("%v\n", r.Perimeter())
	fmt.Printf("%v\n", r.Area())
	fmt.Printf("%T\n", r)
}

```
