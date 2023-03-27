# Language patterns and desighns

## End blocks

So we will be using an `end` keyword to end blocks of code.

## Context

Context names are prefixed with a `$`. Context blocks allow a user to end multipe code blocks at a time, and do certain operations that can't normaly be done.

```
loop as $big_loop
  count (i=0 | i++)
    if (i == 10000000000000000)
        break with $big_loop

end $big_loop
```

The following code shows the ways context can be used. we will loop forever and if `i` is equal to some big number then we will break out of the `loop` loop and `count` loop at the same time. The second use case saves us a lot of typing. Bbecause we have a deeply nested block of code we can end all of them at the same time using context. In this example it will end all the blocks inside the `$big_loop` context.

## Macros

Macros are a way of modifing the syntax of a language without any compiler hacks or anything similar. Macros are expanded at token time. So when a patern of tokens is recognised it will expand it with a matching macro.
