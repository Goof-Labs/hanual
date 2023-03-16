rules = {
    "num": "T",
    "T op T": "expr",
}


stk = []
stream = (i for i in ["num", "op", "num"])


while True:
    token = next(stream, None)

    if not token:
        break

    print()
    for rule, reducer in rules.items():
        rule = rule.split(" ")
        rule.reverse()

        pattern = stk.copy()
        pattern.reverse()

        for idx, (left_token, right_token) in enumerate(zip(pattern, rule)):
            print(left_token, " ", right_token)

            if left_token != right_token:
                if not idx >= 1:
                    break

                for _ in range(idx):
                    stk.pop()

                stk.append(reducer)

                print(f"{pattern} -> {rule}")

    stk.append(token)


print(stk)
