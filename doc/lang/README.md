# Hanual Language Docs

Make sure you read this. The docs will start with a "Hello world", followed by the compilation steps, this includes preprocessers to raw syntax and everything in betweene.

---

## Hello World

The entery point for the program in the main function, this can be altered with compiler flags. The main function takes in no arguments, and the boddy of the function requires one function call `print`, where the only required arguments are the `"Hello world"` string.

```text
fn main()
    print("Hello world")
end
```

---

# Preprocessers

What is a preprocesser?

> A preprocesser is code that is executed before any lexical analasys or parsing.

In the langauage they are prefixed with an `@` followed by their name. These can take in arguments such as the `if` preprocesser.

The preprocessers are as followed:

- mcr
- def
- if
- end

### mcr Preprocesser

The `mcr` preprocesser is a Macro. Macros allow us to extend the language with features we may see fit. Macros are a special case and are not expanded while the program is a string, instead they are expanded after the program has been tokenised. This removes edgecases where macros may be expanded inside of strings.

Macros are first defined with the `@mcr` Preprocesser. The macro is divided into two parts. The left and right side. The left side is the code that is elegable for macro expansion and the right is the code that would reult from the expansion.

```text
@mcr left_side -> right_side
```

Both sides are separated by an arrow `->`. The left side should match with a raw token stream as shown.

```text
@mcr <I:name> => <N:num> -> Right_side
```

### Anatomy of a token type

Generic token types are wrapped in angle brackets. These are similar to variables but strongely typed. The token type can be split into two parts separated by the colon `:`. The left is the token type, `I` would signifiy that the token should be an `ID` token and the `N` should be a number type. These types will be in the tabel below.

### Macro types

| Type | Token name | Example                   |
| ---- | ---------- | ------------------------- |
| `I`  | `ID`       | `name_1   `               |
| `N`  | `NUM`      | `3.14159  `               |
| `S`  | `STR`      | `"pi"     `               |
| `?`  | Any token  | Any token in the language |

The non wrapped token types are just literals, in the example, `=>` must be present but is not actually used. The Generic token types are used on the other side of the macro though. Any tokens such as the `=>` are not in the standared lexer so a lexer hook must be made to make the symbol an official token.

The tokens are then moved onto the right side of the expression where only the name needs to be present, but still wrapped in angle brackets. However, the type is not required to be present.

The tokens are then substituted on the right side of the macro, where the formatted macro is then pushed onto the lexical stack.

## Example

Let's say that we want to replace the `fn` keyword with `func`. We can create a macro that will do this. For the demonstrational perposes I will also include the name in the macro, although it would not be neccessery

```text
@mcr func <I:name> -> fn <name>

func main()
end
```

In the pre-processing steps the macro will be matched to the stream

FINISH THIS
