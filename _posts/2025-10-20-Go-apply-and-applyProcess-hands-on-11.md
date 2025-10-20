---
title: "Go apply and applyProcess hands on 11"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go apply and applyProcess hands on 11"

tags: ['go', 'apply', 'and', 'applyprocess', 'hands', 'on']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
package main

import (
	"net/http"
	"html/template"
)


var tpl *template.Template

func init()  {
	tpl = template.Must(template.ParseGlob("hands-on-11/templates/*.gohtml"))
}


func main()  {
	http.HandleFunc("/", index)
	http.HandleFunc("/about", about)
	http.HandleFunc("/contact", contact)
	http.HandleFunc("/apply", apply)
	http.ListenAndServe(":8080", nil)
}

func index(w http.ResponseWriter, r *http.Request)  {
	tpl.ExecuteTemplate(w, "index.gohtml", nil)
}

func about(w http.ResponseWriter, r *http.Request)  {
	tpl.ExecuteTemplate(w, "about.gohtml", nil)
}

func contact(w http.ResponseWriter, r *http.Request)  {
	tpl.ExecuteTemplate(w, "contact.gohtml", nil)
}

func apply(w http.ResponseWriter, r *http.Request)  {

	if r.Method == http.MethodPost {
		tpl.ExecuteTemplate(w, "applyProcess.gohtml", nil)
		return
	} else {
		tpl.ExecuteTemplate(w, "apply.gohtml", nil)
		return
	}


}



// tree hands-on-11
// hands-on-11
// ├── main.go
// └── templates
//     ├── about.gohtml
//     ├── apply.gohtml
//     ├── applyProcess.gohtml
//     ├── contact.gohtml
//     └── index.gohtml

// 	for i in \ls  hands-on-11/templates/*; do echo "\n\n-----------------------\n//${i}\n"; cat ${i}; done


// 	-----------------------
// 	//ls

// 	cat: ls: No such file or directory


// 	-----------------------
// 	//hands-on-11/templates/about.gohtml

// 	<!DOCTYPE html>
// 	<html lang="en">
// 	<head>
// 		<meta charset="UTF-8">
// 		<title>ABOUT</title>
// 	</head>
// 	<body>

// 	<strong>ABOUT</strong><br>
// 	<a href="/">index</a><br>
// 	<a href="/about">about</a><br>
// 	<a href="/contact">contact</a><br>
// 	<a href="/apply">apply</a><br>

// 	</body>
// 	</html>

// 	-----------------------
// 	//hands-on-11/templates/apply.gohtml

// 	<!DOCTYPE html>
// 	<html lang="en">
// 	<head>
// 		<meta charset="UTF-8">
// 		<title>APPLY</title>
// 	</head>
// 	<body>

// 	<strong>APPLY</strong><br>
// 	<a href="/">index</a><br>
// 	<a href="/about">about</a><br>
// 	<a href="/contact">contact</a><br>
// 	<a href="/apply">apply</a><br>
// 	<form method="POST" action="/apply">
// 		<input type="submit" value="apply">
// 	</form>

// 	</body>
// 	</html>

// 	-----------------------
// 	//hands-on-11/templates/applyProcess.gohtml

// 	<!DOCTYPE html>
// 	<html lang="en">
// 	<head>
// 		<meta charset="UTF-8">
// 		<title>APPLY PROCESS</title>
// 	</head>
// 	<body>

// 	<strong>APPLY PROCESS</strong><br>
// 	<a href="/">index</a><br>
// 	<a href="/about">about</a><br>
// 	<a href="/contact">contact</a><br>
// 	<a href="/apply">apply</a><br>

// 	</body>
// 	</html>

// 	-----------------------
// 	//hands-on-11/templates/contact.gohtml

// 	<!DOCTYPE html>
// 	<html lang="en">
// 	<head>
// 		<meta charset="UTF-8">
// 		<title>CONTACT</title>
// 	</head>
// 	<body>

// 	<strong>CONTACT</strong><br>
// 	<a href="/">index</a><br>
// 	<a href="/about">about</a><br>
// 	<a href="/contact">contact</a><br>
// 	<a href="/apply">apply</a><br>

// 	</body>
// 	</html>

// 	-----------------------
// 	//hands-on-11/templates/index.gohtml

// 	<!DOCTYPE html>
// 	<html lang="en">
// 	<head>
// 		<meta charset="UTF-8">
// 		<title>INDEX</title>
// 	</head>
// 	<body>

// 	<strong>INDEX</strong><br>
// 	<a href="/">index</a><br>
// 	<a href="/about">about</a><br>
// 	<a href="/contact">contact</a><br>
// 	<a href="/apply">apply</a><br>

// 	</body>
// 	</html>%
```
