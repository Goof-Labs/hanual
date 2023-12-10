from __future__ import annotations


import dis
from typing import Any

# special thanks to https://gist.github.com/reza-bagheri


def get_op_arg(offset: int,
               opcode: int,
               arg_val: Any,
               constants: list[Any],
               var_names: list[str],
               names: list[str],
               cell_names: list[str]) -> int:
    op_arg = arg_val
    if opcode in dis.hasconst:
        if constants is not None:
            op_arg = constants.index(arg_val)
    elif opcode in dis.hasname:
        if names is not None:
            op_arg = names.index(arg_val)
    elif opcode in dis.hasjrel:
        arg_val = int(arg_val.split()[1])
        op_arg = arg_val - offset - 2
    elif opcode in dis.haslocal:
        if var_names is not None:
            op_arg = var_names.index(arg_val)
    elif opcode in dis.hascompare:
        op_arg = dis.cmp_op.index(arg_val)
    elif opcode in dis.hasfree:
        if cell_names is not None:
            op_arg = cell_names.index(arg_val)
    return op_arg


def assemble(
        code_list: list[tuple[str, Any]],
        constants: list[Any],
        var_names: list[str],
        names: list[str],
        cell_names: list[str]) -> bytes:
    byte_list = []
    for i, instruction in enumerate(code_list):
        if len(instruction) == 2:
            opname, arg_val = instruction
            opcode = dis.opname.index(opname)
            op_arg = get_op_arg(i * 2, opcode, arg_val, constants, var_names, names, cell_names)
        else:
            opname = instruction[0]
            opcode = dis.opname.index(opname)
            op_arg = 0
        byte_list += [opcode, op_arg]
    return bytes(byte_list)
