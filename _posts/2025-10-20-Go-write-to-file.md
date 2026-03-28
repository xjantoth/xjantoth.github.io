---
title: "Go write to file"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to create and write an HTML file in Go using os.Create, strings.NewReader, and io.Copy."

tags: ['go', 'to', 'file']
categories: ["Go"]
---

This example demonstrates how to write content to a file in Go. It constructs an HTML string using string concatenation, creates a new file with `os.Create`, and then writes the content using `io.Copy` combined with `strings.NewReader`. The `defer` statement ensures the file is properly closed after writing.

```go
package main

import (
	"os"
	"io"
	"fmt"
	"log"
	"strings"
)

func main()  {
	// strongly typed channel
	name := "Jan"
	tpl := `
	<html>
		<body>
			<h1>Hi, this is:` + name + ` </h1>
		</body>
	</html>
	`
	fmt.Printf("%v\n", tpl)

	newFile, err := os.Create("index.html")
	if err != nil {
		log.Fatal("error creating file")
	}
	defer newFile.Close()

	io.Copy(newFile, strings.NewReader(tpl))

}

```
