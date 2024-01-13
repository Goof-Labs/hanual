
# .\setup.py

---

# .\dev\tools\document\doc_parser.py

---

# .\dev\tools\document\template.py

---

# .\dev\tools\document\__main__.py

---

# .\src\hanual\__init__.py

---

# .\src\hanual\__main__.py

---

# .\src\hanual\api\load_hooks.py

---

# .\src\hanual\api\__init__.py

---

# .\src\hanual\api\hooks\hook.py

---
## props.props
> Used to define properties on a GenericHook

 A class decorator that is used to define properties
 on a class.
 Example

 @props(some_prop="some_value")

 - kwargs `dict[str, any]`

   properties to define

   Takes any keywprd argument and attaches them to a Hook, this hook must inherit from `GenericHook`. 



## GenericHook.props
> Used to get the properties defined by `@props`

No provided description


# .\src\hanual\api\hooks\preprocessor.py

---
## new_preprocessor.new_preprocessor
> A decorator to define a new preprocessor Hook

 This is a class decorator that needs to be used to define a
 new preprocessor hook. For example,

 ```py
 @new_preprocessor(skip=["@", "!", "banana"])
 class MyPreprocessor(PreProcessorHook):
     pass
 ```

 - skip `list[LiteralString]`

   A list of characters the preprocessor will skip over.

   The preprocessor will iterate over every line in some code. If the line starts with one of the elements in `skip`, the line will be skipped. 



## PreProcessorHook.scan_lines
> A function that yields lines of code.

 This function takes in the lines of the python file as a generator,
 and yields lines of code. An example use case would be:

 ``` py
 def scan_lines(self, lines):
     for line in lines:
         if "lol" in line:
             continue

         yield line
 ```

 The above example would only yeild lines without the term "lol" in
 them. This means that all lines containing "lol" will not be included
 in the lexed and parsed code.

 - lines `Generator[str, None, None]`

   The lines of source code to preprocess.

   The function is fed the lines of source code as a generator. 


 - return `Generator[str, None, None]`

   The function should be a gen

   The gen should yield all lines or modified lines that it wants to be lexed or parsed. 



## PreProcessorHook.skip
> A list of strings the preprocessor will step over

 This property tells the preprocessor what lines to skip over.
 The preprocessor will digest/process all



# .\src\hanual\api\hooks\rule.py

---
## new_rule.new_rule
> A class decorator for a RuleHook.

 This is a decorator used to decorate a RuleHook. The decorator
 takes in paramiters and sets them as attributes on the RuleHook.
 The paramiters are verry reminicent of the ones used in the
 `parser.rule` decorator. Example:

 @new_rule("some pattern", "pattern two")
 class MyRule(RuleHook):
     pass

 - pattern `tuple[LiteralString]`

   Patterns that match to the rule

   The patterns are a string that outlines what pattern the rule matches up to. e.g. "thing1 thing2 thing3", in this case the rule would only be run if there was a pattern on the stack with [rule1 rule2 rule2]. 


 - prod `Optional[Type]`

   The production passed to the rule

   The production is a class that prepresents elements on the stack. For example, a `DefaultProduction` will be passed to the rule by default, however you can use different, or your own productions if you want. 


 - unless_starts `Optional[Iterable[LiteralString]]`

   New tokens that will prevent the rule from running.

   A list of token types. If the previous token type is listed in the list then the rule will not be run. For example, if we want a rule that simplifies [ A B ] => AB but only if C is not directley before the match e.g. [C A B]. In this example C could be listed in the unless_starts param. 


 - unless_ends `Optional[Iterable[LiteralString]]`

   Tokens at the stack bottom that will prevent the rule from running.

      


 - types `Optional[Dict[LiteralString, Any]]`

   The types of matches asociated.

      


 - name `Optional[str]`

   Custom name for the rule.

      




# .\src\hanual\api\hooks\token.py

---
## new_token.new_token
> A decorator to define a new token.

 This decorator is used to decorate a token class, said class must
 inherit from `TokenHook`. This function doesn't register the token
 but is a cleaner way to define the class attributes.

 - regex `tuple[str, LiteralString]`

   

   




# .\src\hanual\api\hooks\__init__.py

---

# .\src\hanual\compile\compiler.py

---

# .\src\hanual\compile\context.py

---

# .\src\hanual\compile\hanual_function.py

---

# .\src\hanual\lang\builtin_lexer.py

---

# .\src\hanual\lang\builtin_parser.py

---

# .\src\hanual\lang\lexer.py

---
## kw.kw
> Used to define a keyword in the lexer.

 The function us used with in the lexer. This function lets the user define keywords. For example, if you want to
 make a keyword called `let` you could use this function.

 ```py
 kw("let")
 ```

 - reg `LiteralString`

   Name of the keyword.

   The value of the keyword, e.g. `let`, `if` 



## rx.rx
> Used to define a token in the lexer.

 The function us used with in the lexer. This function lets the user define patterns/tokens. For example, if you
 want to make a symbol, `|>` you could use this function with a regular expression that matches the token.

 ```py
 rx(r"\|\>")
 ```

 - reg `LiteralString`

   Value of the regex.

   The pattern of the token, e.g. [a-zA-Z_][a-zA-Z0-9_]+ 




# .\src\hanual\lang\pparser.py

---
## PParser.check_redundancy
> This function checks for redundancy. It

No provided description

## PParser.rule
> This function is a decorator, so it can be used with the following syntax

 parser = PParser()
 ...
 @parser.rule("rule_1", "rule_2")
 def my_rule(*token_stream):
     return "whatever I feel like"
 ...
 ...
 @parser.rule("rule_1", "rule_2", "rule_3", types={
     "rule_1": 1, "rule_2": 2, "rule_3": 3
 })
 def some_rule(*ts, case: int):
     if case == 1: # do some stuff for the first case
     elif case == 2: # other stuff for second case
     elif case == 3: # third case
 @par.rule("NAME LPAR RPAR", unless={"start": "FN"})
 def function_call(ts):
     return ...


## PParser.always
> This will always run on each reduction of the stack or after every check.

No provided description


# .\src\hanual\lang\productions.py

---

# .\src\hanual\lang\token.py

---

# .\src\hanual\lang\__init__.py

---

# .\src\hanual\lang\data\literal_wrapper.py

---

# .\src\hanual\lang\data\__init__.py

---

# .\src\hanual\lang\errors\errors.py

---

# .\src\hanual\lang\errors\trace_back.py

---

# .\src\hanual\lang\errors\__init__.py

---

# .\src\hanual\lang\nodes\algebraic_expr.py

---

# .\src\hanual\lang\nodes\algebraic_fn.py

---

# .\src\hanual\lang\nodes\anon_function.py

---

# .\src\hanual\lang\nodes\arguments.py

---

# .\src\hanual\lang\nodes\assignment.py

---

# .\src\hanual\lang\nodes\base_node.py

---
## BaseNode.prepare
> Used to collect information from the node.

 Provides all necessary info to the compiler such as variable names and
 constants.

 - return `Generator[Response | Request, Reply, None]`

   A gen that provides information to the compiler.

   This gen takes in a compiler Reply and yields either a Request or a reply. The gen should yield data or a request to the compiler and take a reply in this sense, this gen is bidirectional. 



## BaseNode.gen_code
> Generates the code for the compiler to omit.

No provided description


# .\src\hanual\lang\nodes\base_node_meta.py

---

# .\src\hanual\lang\nodes\binop.py

---

# .\src\hanual\lang\nodes\block.py

---
## CodeBlock.__init__
> Initializer of the CodeBlock class.

No provided description


# .\src\hanual\lang\nodes\break_statement.py

---

# .\src\hanual\lang\nodes\conditions.py

---

# .\src\hanual\lang\nodes\dot_chain.py

---

# .\src\hanual\lang\nodes\elif_statement.py

---

# .\src\hanual\lang\nodes\else_statement.py

---

# .\src\hanual\lang\nodes\for_loop.py

---

# .\src\hanual\lang\nodes\freeze_node.py

---

# .\src\hanual\lang\nodes\f_call.py

---

# .\src\hanual\lang\nodes\f_def.py

---

# .\src\hanual\lang\nodes\hanual_list.py

---

# .\src\hanual\lang\nodes\if_chain.py

---

# .\src\hanual\lang\nodes\if_statement.py

---

# .\src\hanual\lang\nodes\implicit_binop.py

---

# .\src\hanual\lang\nodes\implicit_condition.py

---

# .\src\hanual\lang\nodes\iter_loop.py

---

# .\src\hanual\lang\nodes\loop_loop.py

---

# .\src\hanual\lang\nodes\namespace_acessor.py

---

# .\src\hanual\lang\nodes\new_struct.py

---

# .\src\hanual\lang\nodes\parameters.py

---

# .\src\hanual\lang\nodes\range_node.py

---

# .\src\hanual\lang\nodes\return_stmt.py

---

# .\src\hanual\lang\nodes\shout_node.py

---

# .\src\hanual\lang\nodes\strong_field.py

---

# .\src\hanual\lang\nodes\strong_field_list.py

---

# .\src\hanual\lang\nodes\struct_def.py

---

# .\src\hanual\lang\nodes\s_getattr.py

---

# .\src\hanual\lang\nodes\using_statement.py

---

# .\src\hanual\lang\nodes\using_statement_alt_name.py

---

# .\src\hanual\lang\nodes\var_change.py

---

# .\src\hanual\lang\nodes\while_statement.py

---

# .\src\hanual\lang\nodes\__init__.py

---

# .\src\hanual\lang\preprocess\preprocesser.py

---

# .\src\hanual\lang\preprocess\__init__.py

---

# .\src\hanual\lang\util\compile_code.py

---

# .\src\hanual\lang\util\deprecated.py

---
## deprecated.deprecated
> This is a decorator which can be used to mark functions

No provided description


# .\src\hanual\lang\util\dump_tree.py

---

# .\src\hanual\lang\util\line_range.py

---

# .\src\hanual\lang\util\proxy.py

---

# .\src\hanual\util\errors.py

---

# .\src\hanual\util\protocalls.py

---

# .\src\hanual\util\__init__.py

---
