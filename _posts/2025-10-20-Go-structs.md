---
title: "Go structs"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Working with structs in Go including struct definitions, anonymous structs, struct embedding, and struct tags for reflection."

tags: ['go', 'structs']
categories: ["Go"]
---

This example covers several aspects of Go structs: defining a named struct with exported fields, creating anonymous (inline) structs, embedding one struct inside another for composition, and using struct tags with the `reflect` package. Struct embedding in Go provides a form of inheritance where the embedded struct's fields are promoted to the outer struct.

```go
package main

import (
	"fmt"
	// "strconv"
	// "math"
	"reflect"
)


// general way how to define struct
type Doctor struct {
	// if you capitalize key names -> these will be visible for all the other packages
	Number int
	ActorName string
	Companion []string
}


// anonymous struct
// bDoctor := struct{name string}{name: "John Dou"}

func structs()  {
	a := Doctor{
		Number: 3,
		ActorName: "Jon Dou",
		Companion: []string{
			"one",
			"two",
			"three",
		},
	}


	fmt.Printf("Printing Doctor struct: %v\n", a)

	fmt.Printf("Printing Doctor actorName: %v\n", a.ActorName)
	fmt.Printf("Printing Doctor number: %v\n", a.Number)
	fmt.Printf("Printing Doctor companion: %v\n", a.Companion)

	// I would call these anonymous struct as "lambda struct"
	b := struct{name string}{name: "John Dou"}

	fmt.Printf("Anonymous struct: %v\n", b)
	fmt.Printf("Anonymous struct name: %v\n", b.name)


}


type Animal struct {
	Name	string
	Origin	string
}

type Bird struct {
	// embedding "Animal" struct
	Animal
	SpeedKPH	float32
	CanFly		bool
}
	// tagging

type WebAPP struct {
	Name string `required max:"100"`
	Origin string
}


func embedding()  {
	a := Bird{}
	// 1st way how to declare object
	a.Name     = "Emu"
	a.Origin   = "Australia"
	a.SpeedKPH = 48
	a.CanFly   = false

	fmt.Printf("Embedded struct: %v\n", a)

	// 2nd way how to declare Bird object

	x := Bird{
		Animal: Animal{
			Name: "Emu",
			Origin: "Australia",
		},
		SpeedKPH: 30,
		CanFly: false,
	}

	fmt.Printf("Embedded struct: %v\n", x)

	// tagging
	t := reflect.TypeOf(WebAPP{})
	field, _ := t.FieldByName("Name")
	fmt.Printf("%v, %T\n", field.Tag, field.Tag)


}

func main()  {
	// arrays()
	// slices()
	// maps()
	// structs()
	embedding()
}
```
