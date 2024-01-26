# The Hanual language

The hanual language is a compiled language that aims to provide full interopability with CPython. Hanual achives this by compiling all hanual code to CPython's bytecode allowing it to run nativley on the python virtual machine.

## State/Status

At the moment the language is not ready for production at all, to this point there have been no announced versions of the language, however I am planning to push the language forward. Below you can read a checklist, I want in the language before I am declaring a version `0.0.0`

 - [ ] Full support for all nodes
 - [ ] Propper Error messages
 - [ ] Adding static analysis to the compiler
 - [ ] Adding hooks and improving the language API
 - [ ] Implementing errors and error messages
 - [ ] Documentation
 - [ ] A standard library
 - [ ] Build scripts, to build a hanual code base
 - [ ] Compiler optimizations
 - [ ] A python build of the language so that larger projects can use the language
 - [ ] IDE support

## Features

The language aims to have many features that are desired in modern programming. These include primerily concepts that have, likley, been rejected PEPs. This is because python does not want to implement any unpythonic features. However, there are some featues that I have implemented because I believe python would benefit from them:

 - A Switch\Case statement (different from match/case)
 - Multiline anonymous functions
