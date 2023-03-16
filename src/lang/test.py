rules = {
    "A B": "1",
    "A B C": "1",
}


stk = []
stream = (i for i in ["A", "B", "C", "D", "E", "F"])


while True:
    token = next(stream, None)

    if not token:
        break

    stk.append(token)

    pattern = stk.copy()
    pattern.reverse()

    for rule, reducer in rules.items():
        rule = rule.split(" ")
        print(rule, " => ", reducer)

        rule.reverse()

        max_deb = 0
        for i, (r, p) in enumerate(zip(rule, pattern)):
            max_deb = i

            if r != p:
                break

        else:  # The pattern matched perfectly
            [
                stk.pop() for _ in range(max_deb + 1)
            ]  # pop the top n elements of the stack
            stk.append(reducer)

    print("stk ~ ", pattern, "\n")
