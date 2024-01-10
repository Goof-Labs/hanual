The compiler is split into several parts:
- pre-processing
- lexical analysis
- parsing
- optimization
- code generation
***
# Pre-processing
Pre-processing is raw text processing done before lexical analysis. For example, including or excluding code from the final build depending on compiler settings/version/platform et cetera. In hanual the code is divided into lines. The lines are then iterated over in order, if a line starts with the `@` character, the line is then checked. If the word after the "at" is one of:
- def
- end
- nif
- if
### def
`def` is a shorthand for define, it lets the user define a name. The name is appended to a list of names, and stored in the pre-processor.
#### Example
```c
// before this point the `some_name` name has not been defined
@def some_name
// after this point the `some_name` name has been defined
```
### end
`end` resets a flag in the `Preprocessor` class (the flag being `_ignore_code`) to the value of `True`. This is used to end an `if` statement pre-processor.
#### Example
```c
// before this point the `_ignore_code` flag is whatever value it is
@end
// after this point the `_ignore_code` flag is reset to `False`
```
### nif
`nif` is a shorthand for `not if` or `negation if`. This pre-processor checks the name after it, if the specified name is not in the list of names (defined by `def`) the `_ignore_code` flag is set to `True`. As such all code is ignored until the `end` pre-processor.
#### Example
```c
@def a_preprocessor

@nif some_name

// This code will be included because `some_name` has not been defined

@end

// code after this point is included, because the flag has been reset

```
### if
`if` checks if the specified name is in the list of defined names, if it is the following code is included otherwise it is ignored. This too resets the `_ignore_code` flag in the class.
#### Example
```c
@def a_preprocessor

@if some_name

// This code will not be included because `some_name` has not been defined

@end

// code after this point is included, because the flag has been reset
```
## Implementation
> The files can be found in the `src/hanual/lang/preprocess` dir.

The file contains one class `Preprocessor`.
### constructor
The constructor of the class optionally takes a list of strings listing all compiler defined definitions, the `prefix` is a string that defines what character(s) pre-processors are prefixed with.
- `pre_defs`, used to define the definitions of the compiler
- `prefix`, the prefix of the pre-processors
- `hooks`, a list of hooks that are attached to the compiler

### (prop) `prefix`
Returns the prefix of the pre-processors.
### (setter) `prefix`
Sets the prefix of the pre-processor.
### `add_definition`
Adds a definition to the list of definitions.
### `process`
This method is a generator that processes every line in the file, and yields the lines of code to include.
- `text`, this is the source code to be processed
- `prefix`, the prefix for the pre-processor (does override the prefix stored in the class)
- `starting_defs`, the definitions for the compiler (is added to any existing definitions stored in the class)
- `mappings`, a dictionary storing the pre-processor names and functions ([[#`mappings` example|more info]])
#### `mappings` example
Mappings is used to store a dictionary of pre-processor names and functions. For example:
```python
pre_processor.process(
  text=...,
  mappings={
    "hello": "hello_proc"
  }
)
```
In this example when the user uses a pre-processor called `hello` the pre-processor will call the method `_get_hello_proc`. Note the name mangling always follows the form `_get_[METHOD-NAME]`. This method will only be passed the line that caused the match, and should return a modified line or an empty string. For example
```python
class MyPreprocessor(Preprocessor):
  def _get_hello_proc(self, line: str):
	print(f"The line {line!r} was a match!")
    return "println('Hello preprocessor here!')"

my_preproc = MyPreprocessor()
output = my_preproc.process(
  text="@hello",
  mappings={
    "hello": "hello_proc"
  }
)

print(list(output))
# prints:
# The line '@hello' was a match!
# Code:
# println('Hello preprocessor here!')
```

***
# Lexical analysis
The lexer is responsible for breaking the source code string into tokens; this is the first level of abstraction of the compiler. For example, in the code:
```rust
fn main() {
  println("Hello world!")
}
```
The lexer would produce the following tokens:
```python
Token(TK_KEYWORD, value="fn")
Token(TK_ID, value="main")
Token(TK_LPAR, value="(")
Token(TK_RPAR, value=")")
Token(TK_LBRACE, value="{")
Token(TK_ID, value="println")
Token(TK_LPAR, value="(")
Token(TK_STR, value="Hello world")
Token(TK_RPAR, value=")")
Token(TK_RBRACE, value="}")
```
> NOTE: This is only an approximate example of the tokens actually look like

This allows the compiler to deal with a more intuitive representation of the program than one large string.
## Implementation
The tokenizer is split into two files, one being the lexer class and the other being the hanual lexer (found here: `src/hanual/lang/lexer.py` and `src/hanual/lang/builtin_lexer.py`).
### (function) kw
This function is used to define a keywork token. The first parameter is the text that would match said keyword, such as `let`, `and` and so on.
### (function) rx
This function is used to define a new token that should match with the provided regex string. The first parameter is the regular expression to match.
### Lexer
The lexer is 