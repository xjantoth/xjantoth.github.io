---
title: "Go primitives"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go primitives"

tags: ['go', 'primitives']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
// Primitives

func primitives()  {
	var n bool = true
	v := 1 == 1
	x := 3 == 2

	// signed int16 (-65 535, 65 535)
	var c int16 = 2
	// unsigned int16 (0, 65 535)
	var f uint16 = 10

	fmt.Printf("\nPrimitives:\n")
	fmt.Printf("Printig simple boolean: %v, %T\n", n, n)
	fmt.Printf("Is that expresion with variable v: %v and how about x variable: %v\n", v, x)
	fmt.Printf("example of signed int16: %v, %T\n", c, c)
	fmt.Printf("example of unsigned int16: %v, %T\n", f, f)
}


func operations() {
	a := 10   // 1010
	b := 3    // 0011

	println(a + b)
	println(a - b)
	println(a * b)
	println(a / b)
	println(a % b)

	// Bit operators
	print("Printing binary operations:\n")
	println(a & b)  // 0010 = 2
	println(a | b)  // 1011 = 11
	println(a ^ b)  // 1001 = 9
	println(a &^ b) // 0100 = 8

	// Bit shifting
	print("Bit shifting operations:\n")

	d := 8   // 2^8
	fmt.Println(d << 3) //  2^3  * 2^3 = 2^6  -> 64
	fmt.Println(d >> 3) //  2^3  / 2^3 = 2^0  -> 1

	// floating point numbers

	var n float64 = 3.141
	h := 2.14
	v := 13.7e72
	l := 2.1E14

	fmt.Printf("Printing floating number\n")
	fmt.Printf("%v, %v, %v, %v\n", n, h, v, l)

	// complex numbers
	fmt.Printf("Starting with complex numbers:\n")

	var q complex64 = 1 + 2i
	var o complex64 = 2 + 5.2i
	fmt.Printf("Complex numbers: %v, %T\n", q, q)
	println(q + o)
	println(q - o)
	println(q * o)
	println(q / o)

	var u complex128 = 1 + 5i
	fmt.Printf("Complex numbers (real part): %v, %T\n", real(u), real(u))
	fmt.Printf("Complex numbers (imaginary part): %v, %T\n", imag(u), imag(u))

	// another way how to define complex number
	var t complex128 = complex(1, 3)
	fmt.Printf("Complex numbers: %v, %T\n", t, t)

	// string operations

	var s string = "This is my long string"
	fmt.Printf("\nStrings:\n")
	fmt.Printf("%v, %T, %v\n", s, s, string(s[0:20]))


}


func main()  {
	variables()
	primitives()
	operations()
}
```
