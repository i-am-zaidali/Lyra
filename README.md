<h1 align="center"> Lyra </h3>

<h3 align="center"> A linear algebra python project </h3>


A small project I started in my free time to be able to work with linear equations in python

This is a WIP and probably not really gonna be useful for anyone when it's done.

The project is currently in the process of being written and tested.

Docs: `Coming Soon`


## Why "Lyra"?

Lyra was originally named "Li-ra", which stands for "Li(near)-(Algeb)ra" but for some reason i thought a y would suit better here.

## How to use it?

Lyra contains 2 major classes as of now and 3 helper methods.

### Classes:

1. Point
2. Line
3. Triangle

<h4> Point </h4>

The Point class is used to represent cartesian coordinates.

It's a dataclass with 2 attributes. Namely, x and y.

<h4> Line: </h4>

The line class is used to represent a straight line in 2D space.

It should not be instantiated directly by the user but instead using the class methods provided.

<h4> Triangle: </h4>

The triangle class is used to represent a triangle in 2D space.

You can either instantiate this class by passing in 3 line equations representing each side of a triangle
or by using the `.from_vertices` method and passing in three `Point` objects representing each vertex of the triangle.