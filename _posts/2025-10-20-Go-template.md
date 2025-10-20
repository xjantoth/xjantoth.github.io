---
title: "Go template"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go template"

tags: ['go', 'template']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
package main

import (
	"os"
	// "io"
	"fmt"
	"log"
	// "strings"
	"text/template"
)

var tpl *template.Template

func init() {
	fmt.Println("Initializing ...")
	tpl = template.Must(template.ParseGlob("*.gohtmlx"))
}

func main()  {
	// strongly typed channel
	// err := tpl.Execute(os.Stdout, nil)
	// if err != nil {
	// 	log.Fatalln(err)
	// }

	err := tpl.ExecuteTemplate(os.Stdout, "3.gohtml", nil)
	if err != nil {
		log.Fatalln(err)
	}
}

```

**More advanced examples''

```go
package main

import (
	"os"
	// "io"
	"fmt"
	"log"
	// "strings"
	"text/template"
)

var tpl *template.Template

func init() {
	fmt.Println("Initializing ...")
	tpl = template.Must(template.ParseGlob("*.gohtml"))
}

type kernelMember struct {
	Name string
	Position int
}

type car struct {
	Manufacturer string
	Model        string
	Doors        int
}

// I am gonna define a "struct" consuming the previous two

type item struct {
	People    []kernelMember
	Transport []car
}

func main()  {

	j := kernelMember{
		Name: "Jan Toth",
		Position: 1,
	}
	v := kernelMember{
		Name: "Vilko",
		Position: 7,
	}
	ja := kernelMember{
		Name: "Jaroslav",
		Position: 3,
	}
	p := kernelMember{
		Name: "Peto",
		Position: 1,
	}
	k := kernelMember{
		Name: "Krissko",
		Position: 1,
	}

	m := car{
		Manufacturer: "Mercedes",
		Model: "Class E",
		Doors: 4,
	}

	f := car{
		Manufacturer: "Ferrari",
		Model: "Lancer",
		Doors: 3,
	}

	// I am going to put this struct "jano" into slice of list

	sliceOfKernelMembers := []kernelMember{j, v, ja, p, k}
	sliceOfCars := []car{m, f}

	data := item{
		People: sliceOfKernelMembers,
		Transport: sliceOfCars,
	}

	err := tpl.ExecuteTemplate(os.Stdout, "tpl.gohtml", sliceOfKernelMembers)
	if err != nil {
		log.Fatalln(err)
	}

	// tpl-neasted.gohtml
	err = tpl.ExecuteTemplate(os.Stdout, "tpl-neasted.gohtml", data)
	if err != nil {
		log.Fatalln(err)
	}

	sliceVariable := []string{"Gandhi", "Buddha", "Jesus"}

	err = tpl.ExecuteTemplate(os.Stdout, "slice.gohtml", sliceVariable)
	if err != nil {
		log.Fatalln(err)
	}

	err = tpl.ExecuteTemplate(os.Stdout, "slice-with-index.gohtml", sliceVariable)
	if err != nil {
		log.Fatalln(err)
	}

	// maps

	mapVariable := map[string]string{
		"India": "Ghandi",
		"America": "MArtin L. King",
		"Love": "Jesus",
	}

	err = tpl.ExecuteTemplate(os.Stdout, "map.gohtml", mapVariable)
	if err != nil {
		log.Fatalln(err)
	}

}

```'
