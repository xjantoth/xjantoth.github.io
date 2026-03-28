---
title: "Go switch statement"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Comprehensive examples of Go switch statements including simple switches, multi-value cases, initializer syntax, tagless switches, type switches, and early exit with break."

tags: ['go', 'switch', 'statement']
categories: ["Go"]
---

This example demonstrates the various forms of Go's switch statement. It covers simple value-based switches, cases with multiple values, initializer syntax (tag syntax), tagless switches that evaluate boolean conditions, type switches using interfaces, and exiting a matched case early with `break`. Unlike many other languages, Go's switch cases do not fall through by default.

```go
package main

import (
	"fmt"
	// "strconv"
	// "math"
	// "reflect"
	// "math"
)


func simpleSwitch()  {
	switch 212 {
	case 1:
		fmt.Printf("one\n")
	case 2:
		fmt.Printf("two\n")
	case 3:
		fmt.Printf("three\n")
	default:
		fmt.Printf("something else!\n")

	}
}

func severalOptionSwitch()  {
	switch 4 {
	case 1, 5, 10:
		fmt.Printf("one, five and ten\n")
	case 2, 4, 6:
		fmt.Printf("two, four, six\n")
	default:
		fmt.Printf("another number\n")
	}
}

func initializerSwitch()  {
	// tag syntax
	fmt.Printf("\nStarting:\n\n")

	switch i := 2 + 3; i {
	case 1, 5, 10:
		fmt.Printf("one, five and ten\n")

	case 2, 4, 6:
		fmt.Printf("two, four, six\n")
	default:
		fmt.Printf("another number\n")
	}

}

func switchWithoutCondition()  {
	// tagless syntax
	i := 10
	switch {
	case i <= 10:
		fmt.Printf("less than or equal to ten\n")
		// be very carefull about this word "fallthrough" because
		// it is mindless and you take the responsibility
		// you do not use this very often!!!
		// ...
		// fallthrough
		// ...
	case i <= 20:
		fmt.Printf("less than or equal to twenty\n")
	default:
		fmt.Printf("greater than twenty\n")

	}
}


func switchUsingInterface()  {
	// var i interface{} = 2
	// var i interface{} = 2.0
	// var i interface{} = "two"
	// var i interface{} = [3]int{}
	var i interface{} = map[string]int{}

	switch i.(type) {
	case int:
		fmt.Printf("i is an int (%T)\n", i)
	case float64:
		fmt.Printf("i is float64 (%T)\n", i)
	case string:
		fmt.Printf("i is a string (%T)\n", i)
	case [3]int:
		fmt.Printf("i is an [3]int (%T)\n", i)
	default:
		fmt.Printf("i is another type (%T)\n", i)
	}
}

func exitSwitchEarly()  {
	var i interface{} = 2
	// var i interface{} = 2.0
	// var i interface{} = "two"
	// var i interface{} = [3]int{}
	// var i interface{} = map[string]int{}

	switch i.(type) {
	case int:
		fmt.Printf("i is an int (%T)\n", i)
		// if you do now want to execute code below
		// within this matched "case" -> please use "break" statement
		break
		fmt.Printf("I do not want to execute this part i is an int (%T)\n", i)

	case float64:
		fmt.Printf("i is float64 (%T)\n", i)
	case string:
		fmt.Printf("i is a string (%T)\n", i)
	case [3]int:
		fmt.Printf("i is an [3]int (%T)\n", i)
	default:
		fmt.Printf("i is another type (%T)\n", i)
	}
}

func main() {
	// simpleSwitch()
	// severalOptionSwitch()
	// initializerSwitch()
	// switchWithoutCondition()
	// switchUsingInterface()
	exitSwitchEarly()
}```
