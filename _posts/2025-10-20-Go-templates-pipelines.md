---
title: "Go templates pipelines"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Using Go template pipelines and custom FuncMap functions for date formatting, math operations, and chaining function calls in templates."

tags: ['go', 'templates', 'pipelines']
categories: ["Go"]
---

This example demonstrates Go template pipelines with custom functions registered via `template.FuncMap`. It defines helper functions for date formatting, doubling a number, computing square roots, and squaring values. These functions are registered on the template engine so they can be called directly within `.gohtml` template files using the pipeline syntax.

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
