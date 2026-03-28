---
title: "Go constants"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Working with constants in Go, including typed and untyped constants, the iota enumerator, and scoped constant blocks."

tags: ['go', 'constants']
categories: ["Go"]
---

This program covers Go constants: typed constants with explicit types, untyped constants that can be implicitly converted, and enumerated constants using `iota`. The `iota` keyword auto-increments within a `const` block and resets in each new block. The example also shows how to offset `iota` values and use the blank identifier to discard the first value.

```go
func constants()  {
	// it is a constant because it should not change its value !!!
	const a int16 = 42
	const b string = "foo"
	const c float32 = 43.1
	const d bool = true

	const x int16 = 22

	// const myConst float64 = math.Sin(1.57) -. will throw an error because it is calculated at runtime
	// myConst = 1 -> will throw an error
	fmt.Printf("Constant: %v, %T\n", a, a)
	fmt.Printf("Constant: %v, %T\n", b, b)
	fmt.Printf("Constant: %v, %T\n", c, c)
	fmt.Printf("Constant: %v, %T\n", d, d)
	fmt.Printf("Constant addition: %v, %T\n", a + x, a + x)

	// mind blower

	const g = 10
	var l int16 = 20
	fmt.Printf("!!! Constant + variable addition: %v, %T\n", g + l, g + l)

}

const (
	xyz = iota
	xyq = iota
	xyf = iota
	// check this -> compiler knows that it should be set as "iota" <- enumerator
	ccc
	ddd
)

const (
	//  "iota" is scoped to a const (...) block
	a1 = iota
	a2 = iota
	a3 = iota
	a4 = iota
)

const (
	_ = iota + 5
	catSpecialist
	dogSpecialist
	snakeSpecialist
)

func enumeratedConstants()  {
	// fmt.Printf("Enumerated constants: %v, %T\n", xyz, xyz)
	fmt.Printf("Enumerated constants: %v\n", xyz)
	fmt.Printf("Enumerated constants: %v\n", xyq)
	fmt.Printf("Enumerated constants: %v\n", xyf)
	fmt.Printf("Enumerated constants: %v\n", ccc)
	fmt.Printf("Enumerated constants: %v\n", ddd)

	fmt.Printf("\nNew const(...) block resets \"iota\"\n\n")

	fmt.Printf("Enumerated constants: %v\n", a1)
	fmt.Printf("Enumerated constants: %v\n", a2)
	fmt.Printf("Enumerated constants: %v\n", a3)
	fmt.Printf("Enumerated constants: %v\n", a4)

	fmt.Printf("\n_ + 5 will be evaluated but thrown away \"iota\"\n\n")
	fmt.Printf("Enumerated constants: %v\n", catSpecialist)
}

func main()  {
	// variables()
	// primitives()
	// operations()
	// arrays()
	// constants()
	enumeratedConstants()
}
```
