# Parse Libruary

The hanuel programing anguage uses a custom made parser.

## Parsing process

> Note that some variable names have been changed to make the parsing prosess easier to understand

The parser will start by getting a token of the `token_stream`, this is parsed into the `parse` function. The current `pattern` has the token type added onto the end of the `pattern` and the token object added onto the `t_pattern`. Next the parser will check through all the rules to see if the `pattern` matches any of the `rule_patterns`, if so then the corasponding fucntion is called. The result is appended onto the `tree`, which is a list of all AST fragments.

### usage

```py
...

@parser.rule("rule_1", "rule_1 rule_2",)
def expr(ts):
  # create ast inside of function
  return new_ast

...
```

The decorator takes any number of arguments, these are the token patterns we would like to specifiy, the token paterns are separated by spaces `" "` so the pattern `"t1 t2 t3 t4"` matches with `t1` followed by `t2` followed by `t3` followed by `t4`, these rules also have no constraint, unless a token name/type has a name has a space in it, hence why token names should not have a space in them.

