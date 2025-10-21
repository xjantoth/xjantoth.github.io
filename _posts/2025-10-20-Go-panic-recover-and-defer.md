---
title: "Go panic() recover() and defer()"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go panic() recover() and defer()"

tags: ['go']
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
	"net/http"
	"log"

)

func simplePanic()  {
	a, b := 1, 0
	ans := a/b
	fmt.Printf("ans: %v\n", ans)
}

func usePanic()  {
	fmt.Printf("start\n")
	panic("something bad happened")
	fmt.Printf("end\n")
}



func panicInWebAPP()  {
	http.HandleFunc("/", func (w http.ResponseWriter, r *http.Request)  {
		w.Write([]byte("Hello Go!"))
	})

	err := http.ListenAndServe(":8000", nil)
	if err != nil {
		panic(err.Error())
	}

}

func deferIsExecutedBeforePanic()  {
	fmt.Printf("start\n")
	defer fmt.Printf("this was defered\n")
	panic("something bad happened")
	fmt.Printf("end\n")
}


func xdeferIsExecutedBeforePanic()  {
	fmt.Printf("start\n")
	defer func()  {
		if err := recover(); err != nil {
			log.Printf("Something bad happended error: %v\n", err)
			// if the error is so bad
			// simply use:
			// panic("I cannot handle it anymore :)")
		}

	}()
	panic("Panic something bad happened\n")
	fmt.Printf("end\n")
}


func main() {
	// simplePanic()
	// usePanic()
	// panicInWebAPP()
	xdeferIsExecutedBeforePanic()
	fmt.Printf("end\n")
}
``
