---
title: "Go serving files with StripPrefix() hands on"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go serving files with StripPrefix() hands on"

tags: ['go', 'files', 'hands']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
package main

import (
	"html/template"
	"log"
	"net/http"
)

func main() {

	http.HandleFunc("/", photos)
	http.Handle("/resources/", http.StripPrefix("/resources", http.FileServer(http.Dir("starting-files/public"))))
	log.Fatalln(http.ListenAndServe(":8080", nil))

}



func photos(w http.ResponseWriter, r *http.Request) {
	tpl, err := template.ParseFiles("starting-files/templates/index.gohtml")
	if err != nil {
		log.Fatalln(err)
	}
	tpl.ExecuteTemplate(w, "index.gohtml", nil)
}


// tree starting-files
// starting-files
// ├── public
// │   └── pics
// │       ├── dog1.jpeg
// │       ├── dog2.jpeg
// │       └── dog.jpeg
// └── templates
//     └── index.gohtml


// starting-files/templates/index.gohtml
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>

<h1>Pictures of dogs redux:</h1>
<img src="/resources/pics/dog.jpeg">
<img src="/resources/pics/dog1.jpeg">
<img src="/resources/pics/dog2.jpeg">

</body>
</html>

```
