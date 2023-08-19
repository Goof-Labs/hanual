import types

# https://stackoverflow.com/questions/25568232/how-can-i-recursively-print-the-contents-of-a-variable-including-both-the-data
# Thank you jozxyqk btw I did make this py311 compatible


def dump_tree(obj, depth=4, l=""):
    # fall back to repr
    if depth < 0:
        return repr(obj)
    # expand/recurse dict
    if isinstance(obj, dict):
        name = ""
        objdict = obj
    else:
        # if basic type, or list thereof, just print
        canprint = lambda o: isinstance(
            o, (int, float, str, bool, types.NoneType, types.LambdaType)
        )
        try:
            if canprint(obj) or sum(not canprint(o) for o in obj) == 0:
                return repr(obj)
        except TypeError as e:
            pass
        # try to iterate as if obj were a list
        try:
            return (
                "[\n"
                + "\n".join(
                    l + dump_tree(k, depth=depth - 1, l=l + "  ") + "," for k in obj
                )
                + "\n"
                + l
                + "]"
            )
        except TypeError as e:
            # else, expand/recurse object attribs
            name = (
                hasattr(obj, "__class__")
                and obj.__class__.__name__
                or type(obj).__name__
            )
            objdict = {}
            for a in dir(obj):
                if a[:1] != "_" and (
                    not hasattr(obj, a) or not hasattr(getattr(obj, a), "__call__")
                ):
                    try:
                        objdict[a] = getattr(obj, a)
                    except Exception as e:
                        objdict[a] = str(e)
    return (
        name
        + "{\n"
        + "\n".join(
            l + repr(k) + ": " + dump_tree(v, depth=depth - 1, l=l + "  ") + ","
            for k, v in objdict.items()
        )
        + "\n"
        + l
        + "}"
    )
