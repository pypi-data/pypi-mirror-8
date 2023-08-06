# /cmakeast/ast_visitor.py
#
# A function that recursively visits an AST
#
# See LICENCE.md for Copyright information
"""A function that recursively visits an AST"""

from collections import namedtuple

_AbstractSyntaxTreeNode = namedtuple("_node",
                                     "single multi handler")


def _node(handler, single=None, multi=None):
    """Returns an _AbstractSyntaxTreeNode with some elements defaulted"""
    return _AbstractSyntaxTreeNode(handler=handler,
                                   single=(single if single else []),
                                   multi=(multi if multi else []))

_NODE_INFO_TABLE = {
    "ToplevelBody": _node("toplevel", multi=["statements"]),
    "WhileStatement": _node("while_stmnt", single=["header", "footer"],
                            multi=["body"]),
    "ForeachStatement": _node("foreach", single=["header", "footer"],
                              multi=["body"]),
    "FunctionDefinition": _node("function_def", single=["header", "footer"],
                                multi=["body"]),
    "MacroDefinition": _node("macro_def", single=["header", "footer"],
                             multi=["body"]),
    "IfBlock": _node("if_block", single=["if_statement",
                                         "else_statement",
                                         "footer"],
                     multi=["elseif_statements"]),
    "IfStatement": _node("if_stmnt", single=["header"], multi=["body"]),
    "ElseIfStatement": _node("elseif_stmnt", single=["header"],
                             multi=["body"]),
    "ElseStatement": _node("else_stmnt", single=["header"], multi=["body"]),
    "FunctionCall": _node("function_call", multi=["arguments"]),
    "Word": _node("word")
}


def recurse(node, *args, **kwargs):
    """Recursive print worker - recurses the AST and prints each node"""

    node_name = node.__class__.__name__
    try:
        info_for_node = _NODE_INFO_TABLE[node_name]
    except KeyError:
        return

    action = None

    try:
        action = kwargs[info_for_node.handler]
    except KeyError:
        pass

    try:
        depth = kwargs["depth"]
    except KeyError:
        depth = 0

    # Invoke action if available
    if action is not None:
        action(name=node_name, node=node, depth=depth)

    # Recurse
    recurse_kwargs = kwargs
    kwargs["depth"] = depth + 1

    for single in info_for_node.single:
        recurse(getattr(node, single),  # pylint:disable=star-args
                *args,
                **recurse_kwargs)

    for multi in info_for_node.multi:
        for statement in getattr(node, multi):
            recurse(statement,  # pylint:disable=star-args
                    *args,
                    **recurse_kwargs)
