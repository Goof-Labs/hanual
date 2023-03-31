from __future__ import annotations


class GlobalState:
    __slots__ = "_vals", "_vars"

    """
    The _vals in the class holds the values of the code
    these are constants and can not be changed, so we
    can be more efficient when it comes to runtime
    performance. These can be substituted at compile-time
    
    But what if another program wants to borrow the
    constant? The vals data is a table that is stored at the
    file header. This is identical to a constant pool count.
    The only difference is that the val pool should be
    faster to access. This means that we take less time when
    it comes to borrowing constants from other files.
    """

    def __init__(self):
        ...
