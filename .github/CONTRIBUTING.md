# Contributing

## Setting up

First clone the repo and install the current environment. This means you need to run

```sh
pip install -e .
```

depending on what os you are on.

## Conventions

It is recomended that you use black as your code formatter and follow pyonic naming convensions. You are encoraged to keep the code OOP but use python's features where apropriate, e.g dataclasses, enums, list comprehensions. The thechnical overveiw of what has been changed should be in the PR (pull request) and use the prefix to indicate what changes have been made. These are listed below and should be in square brackets as shown

| Name   | Example                 | For               |
| ------ | ----------------------- | ----------------- |
| `[BF]` | `[BF]` loop jump labels | Bug fixes         |
| `[NF]` | `[NF]` added for loops  | New feature       |
| `[MG]` | `[MG]` using new jumps  | Migration         |
| `[IM]` | `[IM]` better errors    | Improvement       |
| `[RD]` | `[RD]` removed http lib | Remove depricated |
| `[RF]` | `[RF]` main.py Main cls | Refactored        |
| `[AL]` | `[AL]` added http lib   | Add libruary      |
| `[MD]` | `[MD]` update http docs | Modified docs     |
| `[ND]` | `[ND]` documented loops | New docs          |
