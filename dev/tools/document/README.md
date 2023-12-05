# Documentation tool

Hanual uses a custom documentation tool to help document code. The tool requires that all function documentation is done in comments. The below is an example:
```py
def spam(egg: list[int]):
    """Brief summery of the function goes here!

    > A longer summery can go here
    > It can even go across multiple
    > lines!

    @egg^list[int] > A breif summery of the argument
    | Argument use case and example
    | if you want
    | This can also go across multiple lines
    @return^Literal[None] > What the function returns
    """
```

Do note that the tool will default to type hints if an explicit type is not mensioned.
