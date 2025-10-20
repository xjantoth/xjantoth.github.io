---
title: "Go interfaces"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go interfaces"

tags: ['go', 'interfaces']
categories: ["tiddlywiki"]

hiddenFromSearch: false
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
