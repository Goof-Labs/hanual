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

### handeling edge cases

There are also edge cases where, for example, there is an unparseable pattern, take the following example where we have the rules:

#### keeping a token on the stack

Lets say that the parser can do simple addition and parse these equations into a tree.

We start by pushing the token `2` to the stack, the stack cannot be simplified so we push the next token which is `+` this can't be simplified so we push the next token `1`. The stack which is now `[ 1 , + , 2 ]` can now be simplified into a binary opperation. The value is then pushed to the master tree, the stack is also cleared, in the situation where we then push the value `+` and `1`, they would be added onto an empty stack, this would cause the next tokens to be pushed onto an empty stack. So we may want to preserve the result of the last operation in some capacity.

#### Not parsing expressions propperly
```yacc

num |
ID
: data_type

+ |
- |
\ |
*
: BIN_OP

data_type BIN_OP data_type
: expr

expr BIN_OP data_type
: expr
```

If we have the stream `[ 'var_1' '+' '1' ]` this would be parsed no problem and would cause the ollowing senario:

push-new-token `var_1`
`var_1` => `data_type` # This is the simplification that occurs
`data_type` # This is the value on the pattern stack

push-new-token `+`
`data_type` `+` => # This expression cannot be simplified
`data_type` `+`

push-new-token `1`
`data_type` `+` `1` => # problem: The `1` cannot be simplified into a `data_type` because the parser will look for a whole match
`data_type` `+` `1` # < The `1` was not turned into a `data_type` big bug here

