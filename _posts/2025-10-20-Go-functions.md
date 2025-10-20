---
title: "Go functions"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go functions"

tags: ['go', 'functions']
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

func sayMessage(msg string, idx int)  {
	greetings := "Hello"
	fmt.Printf("%v: %v, %v\n", greetings, msg, idx)
}

func sayGreeting(greeting string, name string)  {
	fmt.Printf("%v: %v\n", greeting, name)
}

// a little bit niceier
func niceierSayGreeting(greeting, name string)  {
	fmt.Printf("%v: %v\n", greeting, name)
}

func greetingWithPointer(greeting, name *string)  {
	fmt.Printf("%v: %v\n", *greeting, *name)
	*name = "Ted"
	fmt.Printf("Derefernced name: %v.\n", *name)
}


// variatic parameter, and if such a parameter is used, it needs to
// be specified at the end
func sum(msg string, values ...int)  {
	fmt.Printf("%v, %T\n", values, values)

	result := 0
	for _, v := range values {
		result += v
	}
	fmt.Printf("%v", msg)
	fmt.Printf("Sum of the values is: %v\n", result)
}



func sumWithReturn(msg string, values ...int) (string, int) {
	fmt.Printf("%v, %T\n", values, values)

	result := 0
	for _, v := range values {
		result += v
	}
	fmt.Printf("%v", msg)
	fmt.Printf("Sum of the values is: %v\n", result)
	return msg, result
}

func divide(a, b float64) (float64, error)  {
	if b == 0.0 {
		return 0.0, fmt.Errorf("Cannot divide by zero")
	}
	return a / b, nil
}

func main() {
	for i :=0; i < 5; i++ {
		sayMessage("Hey go!", i)
	}

	fmt.Printf("\n------------------\n")
	sayGreeting("Hello", "Stacey")

	fmt.Printf("\n------------------\n")
	niceierSayGreeting("Hi", "Katka")

	fmt.Printf("\n------------------\n")
	greeting := "Ahoj"
	name := "Tanicka"
	greetingWithPointer(&greeting, &name)

	fmt.Printf("\n------------------\n")
	sum("Has to be specified before variatic parameter\n" ,2, 3, 4, 5)

	fmt.Printf("\n------------------\n")
	m, r := sumWithReturn("Some silly string", 4, 5, 6, 7)
	fmt.Printf("Returning: %v, %v\n", r, m)

	fmt.Printf("\n------------------\n")

	res, err := divide(5.0, 0.0)
	if err != nil {
		fmt.Printf("Here is what happened: %v\n", err)
		return
	}

	fmt.Printf("Division: %v\n", res)

	fmt.Printf("\n------------------\n")

	// anonymus function

	func()  {
		fmt.Printf("This is an anonymous function\n")
	}()
}


# ---------------------------
package main

import (
	"fmt"
	// "strconv"
	// "math"
	// "reflect"
	// "net/http"
	// "log"

)



func main() {
	for i := 0; i < 5; i++ {
		func(x int)  {
			fmt.Printf("Count: %v\n", x)
		}(i)
	}


	f := func(i string)  {
		fmt.Printf("Anonymous as variable: %v\n", i)
	}

	f("XYZ")

	// more complicated example
	var divide func(float64, float64) (float64, error)
	divide = func (a, b float64) (float64, error)  {
		if b == 0.0 {
			return 0.0, fmt.Errorf("Cannot divide by zero!")
		}

		return a / b, nil
	}

	d, err := divide(5.0, 0.1)

	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("Success division: %v\n", d)


}







```
