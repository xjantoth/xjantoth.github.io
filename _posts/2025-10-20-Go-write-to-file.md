---
title: "Go write to file"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go write to file"

tags: ['go', 'to', 'file']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

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
