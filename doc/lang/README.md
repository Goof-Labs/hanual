# The hanul language

## Introduction

The hanual language is a compiled language that compiles to python bytecode. The language resembles parts of python while borowing from languages such as `java` and `c++`.

## Introduced features

### Overloading

Overloading is when you define multiple functions with the same name but with different input types and paramiters. This is used in `java` and `c++`, however many languages don't support this feature. The overloading syntax in hanual follows the same patterns as in other programing languages, you define multipe functions with the same name, with an `overload` decorator. You can define a default overload function with the `overload.def` decorator.

```text
@overload
fn 
```

### Pipe oporator

The pipe oporator is a symbol used in many functional programing languages. It allows the result of one function being passed to another without deep parenthisis nesting.

### Macros

