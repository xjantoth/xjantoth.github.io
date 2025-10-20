---
title: "Go arrays <TITLE><TITLE> slices"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go arrays <TITLE><TITLE> slices"

tags: ['go', 'arrays', 'slices']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
package main

import (
	"fmt"
	// "strconv"
	// "math"
)


func arrays()  {
	grade1 := 97
	grade2 := 85
	grade3 := 93

	grades := [3]int{11,22,33}
	// [...]int{if I do not know how many elements will be stored in array}
	gradesx := [...]int{11,22,33,444}

	fmt.Printf("Grades: %v, %v, %v\n", grade1, grade2, grade3)
	fmt.Printf("%v\n", grades)
	fmt.Printf("%v\n", gradesx)

	var students [3]string
	fmt.Printf("Printing an empty array %v\n", students)

	students[0] = "jano"

	fmt.Printf("Printing filled array %v\n", students)
}

func slices()  {
	a := []int{1,4,7}
	fmt.Printf("Printing slice %v\n", a)
	fmt.Printf("Printing slice length: %v\n", len(a))
	fmt.Printf("Printing slice capacity %v\n", cap(a))

	x := []int{1,2,3,4,5,6,7,8,9,10}

	b := x[:]
	c := x[3:]
	d := x[:6]
	e := x[3:6]

	// changes same underlying data ()
	x[5] = 42

	fmt.Printf("%v\n", x)
	fmt.Printf("%v\n", b)
	fmt.Printf("%v\n", c)
	fmt.Printf("%v\n", d)
	fmt.Printf("%v\n", e)

	// special make() function
	v := make([]int, 3, 100)
	fmt.Printf("Printing slice %v\n", v)
	fmt.Printf("Printing slice length: %v\n", len(v))
	fmt.Printf("Printing slice capacity %v\n", cap(v))


	j := []int{}
	j = append(j, 10)
	j = append(j, 20)
	fmt.Printf("Printing slice %v\n", j)
	fmt.Printf("Printing slice length: %v\n", len(j))
	fmt.Printf("Printing slice capacity %v\n", cap(j))


	t := []int{}
	t = append(t, 88)
	t = append(t, 77, 99)
	//
	t = append(t, []int{11, 22, 55}...)
	fmt.Printf("Printing slice %v\n", t)
	fmt.Printf("Printing slice length: %v\n", len(t))
	fmt.Printf("Printing slice capacity %v\n", cap(t))

}

func main()  {
	// arrays()
	slices()
}
```
