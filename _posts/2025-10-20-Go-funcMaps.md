---
title: "Go funcMaps"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Go programming: Go funcMaps with working code examples."

tags: ['go', 'funcmaps']
categories: ["Go"]
---

```go
package main

import (
	"os"
	// "io"
	"fmt"
	"log"
	"strings"
	"text/template"
)

var tpl *template.Template

func firstThree(s string) string  {
	s = strings.TrimSpace(s)
	s = s[:3]
	return s
}

var fm = template.FuncMap{
	"uc": strings.ToUpper,
	"ft": firstThree,
}

func init() {
	fmt.Println("Initializing ...")
	// tpl = template.Must(template.ParseGlob("*.gohtml"))
	//  to incorporate some extra function into template object
	tpl = template.Must(template.New("").Funcs(fm).ParseGlob("*.gohtml"))
}

type sage struct {
	Name  string
	Motto string
}

func main()  {
	b := sage{
		Name: "Buddha",
		Motto: "The belief of no beliefs",
	}

	g := sage{
		Name: "Gandhi",
		Motto: "Be the change",
	}

	j := sage{
		Name: "Jesus",
		Motto: "Love!",
	}

	sages := []sage{b, g, j}

	data := struct{
		Wisdom []sage
	}{
		Wisdom: sages,
	}

	err := tpl.ExecuteTemplate(os.Stdout, "funcintpl.gohtml", data)
	if err != nil {
		log.Fatalln(err)
	}


}

```
