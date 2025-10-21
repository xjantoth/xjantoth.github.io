---
title: "Go if else statements"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go if else statements"

tags: ['go', 'else', 'statements']
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
)


func ifelsestatements()  {

	statePopulation := make(map[string]int)
    statePopulation = map[string]int{
        "California": 2341232,
        "Texas": 3341232,
        "Florida": 4341232,
        "New York": 5341232,
        "Illinois": 6341232,
        "Ohio": 7341232,
	}
	fmt.Printf("%v\n", statePopulation)

	if population, ok := statePopulation["California"]; ok {
		fmt.Printf("Population of California is: %v\n", population)
	}


	number := 50
	guess := -1

	if guess < 1 {
		fmt.Printf("The guess must be grater than 1!\n")
	}else if guess > 100 {
		fmt.Printf("The guess must be less than 100!\n")
	}else {
		if guess < number {
			fmt.Printf("Too low!\n")
		}
		if guess > number {
			fmt.Printf("Too high\n")

		}
		if guess == number {
			fmt.Printf("Equal\n")
		}
	}
myNum := 0.223456789
	if math.Abs(myNum / math.Pow(math.Sqrt(myNum), 2) -1) < 0.001 {
		fmt.Printf("These are the same!\n")
	} else {
		fmt.Printf("These are different!\n")
	}

}

func main()  {
	// arrays()
	// slices()
	// maps()
	// structs()
	// embedding()
	ifelsestatements()
}
```
