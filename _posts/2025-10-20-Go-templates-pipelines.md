---
title: "Go templates pipelines"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go templates pipelines"

tags: ['go', 'templates', 'pipelines']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
package main

import (
	"os"
	"time"
	"fmt"
	"log"
	"math"
	"text/template"
)

var tpl *template.Template

func init() {
	fmt.Println("Initializing ...")
	// tpl = template.Must(template.ParseGlob("*.gohtml"))
	//  to incorporate some extra function into template object
	tpl = template.Must(template.New("").Funcs(fm).ParseGlob("pipelines.gohtml"))
}

//  define several functions to be used in templating
func monthDayYear(t time.Time) string{
	return t.Format("01-02-2006")
}




func double(x int) int {
	return x + x
}

func sqRoot(x float64) float64 {
	return math.Sqrt(x)
}

func square(x int) float64 {
	return math.Pow(float64(x), 2)
}

var fm = template.FuncMap{
	"fdateMDY": monthDayYear,
	"fdbl": double,
	"fsqrt": sqRoot,
	"fsq": square,
}


func main()  {

	// err := tpl.ExecuteTemplate(os.Stdout, "dateformatting.gohtml", time.Now())
	err := tpl.ExecuteTemplate(os.Stdout, "pipelines.gohtml", 3)

	if err != nil {
		log.Fatalln(err)
	}



}

```
