# Lexing and Parsing libruary

## Introduction

The lexing/tokenizing libruary is custom made for this language. This means that they both have their own quirks and feature that are unique to this project. If you want to use the lexer and parser, you just need to coppy the `lexer.py`, `pparser.py` file into your own project, it is suggested that you also coppy the `productions.py` file.

## How it works

I have created, hopefully, a new parsing method. This method uses two synced stacks the `global_pattern_stack`, `global_token_stack`, the last stack is the pattern stack, which isn't much of a stack. The `gps` keeps track of all the token types, e.g `LPAR`, `NUM`, ... The value of the token, or token data is stored in the `gts`, both stacks have elements pushed and popped at the same points in the code, hence why they are sincoronised. The application programmable interface or API for this parser is verry much `sly` inspired. The user creates a `PParser` instance and uses the `@parser.rule(...)` decorator to define a rule. A rule has three parts:

- Pattern
- Reducer
- Caller

### Pattern

The pattern is a pattern of tokens and other rule names as a string, these are separated by spaces, so in `token_1 rule_34` the pattern requires that `token_1` is preasent followed by `rule_34`. This is the most intuitive way I could find.

### Reducer

Once we have found our pattern, `token_1` followed by `rule_34` we sould reduce this in some manner to show that we have simplifiied this. This is the roll of the reducer and it is what a recognised pattern is replaced by, this is programmed to be the name of the function, verry much like `sly`. So If we had the rule that:

```yacc
token1_with_rule34_after_it:
    token_1 rule_34
```

So if we imagine that we have a token list and we have just found `token_1` followed by `rule_34`, we would pop these tokens off the `gps` and the `gts`, and push `token1_with_rule34_after_it` to replace it.

### Caller

The caller is again, verry `sly` inspired, we pass our tokens in to some function, hence why we use a decorator, and push the name of the function, which is the `reducer`, onto the `gps`, and the return value of the function onto the `gts`.
