# Changelog

## Introduction

The changelog includes changes to the codebase on a regular basis. For now conventunal purposes be donw in the following format.

```markdown
## [Brief overview of change]

[notes about the change]

## [compatability problems]

[code that will need to be addressed or optimized]

## [next steps]

[The next cours of action]
```

## Finished parser

The parser is now production ready, I have removed the test file.

## compatability problems

Need to check if the main file still works.

## next steps

I want to add various productions to the parser, where the parser will return a production class, this will let the user be able to get elements out of the oken stream more eleigently. Similar to yacc. The reason why I want to add multiple of them is because some of them may not be pythonic or may just suit some situations better then others.

```py
# The following code shows why multiple productions may be neccessery or usefull
# They all show different ways to access the first token

@parser.parse("rules", prod=default)
def abc(ts):
    return ts[0]

@parser.parse("rules", prod=Prod1)
def abc(ts):
    return ts.get_token(0)

@parser.parse("rules", prod=Prod2)
def abc(ts):
    return ts.rules

@parser.parse("rules", prod=Prod3)
def abc(ts):
    return ts[0]

```

I also want to add choices to may parser, because the parser can have multiple rules for each function, I also want to add ways to diferenciate. This servers a simmilar purpose to the various productions.
