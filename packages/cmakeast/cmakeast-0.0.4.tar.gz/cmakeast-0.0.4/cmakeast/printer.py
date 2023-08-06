# /cmakeast/printer.py
#
# Dumps an AST for a specified FILE on the commandline
#
# See LICENCE.md for Copyright information
"""Dumps an AST for a specified FILE on the commandline"""

from cmakeast import ast, ast_visitor
import argparse
import sys


def _parse_arguments():
    """Returns a parser context result"""
    parser = argparse.ArgumentParser(description="CMake AST Dumper")
    parser.add_argument("filename", nargs=1, metavar=("FILE"),
                        help="read FILE")
    return parser.parse_args()


def _print_details(extra=None):
    """Returns a function that prints node details"""
    def print_node_handler(name="", node=None, depth=0):
        """Standard printer for a node"""
        line = "{0}{1} {2} ({3}:{4})".format(depth,
                                             (" " * depth),
                                             name,
                                             node.line,
                                             node.col)
        if extra is not None:
            line += " [{0}]".format(extra(node))

        sys.stdout.write(line + "\n")

    return print_node_handler


def do_print(filename):
    """Print the AST of filename"""
    with open(filename) as cmake_file:
        body = ast.parse(cmake_file.read())

        word_print = _print_details(lambda n: "{0} {1}".format(n.type,
                                                               n.contents))
        ast_visitor.recurse(body,
                            while_stmnt=_print_details(),
                            foreach=_print_details(),
                            function_def=_print_details(),
                            macro_def=_print_details(),
                            if_block=_print_details(),
                            if_stmnt=_print_details(),
                            elseif_stmnt=_print_details(),
                            else_stmnt=_print_details(),
                            function_call=_print_details(lambda n: n.name),
                            word=word_print)


def main():
    """Parse the filename passed on the commandline and dump its AST


    The AST will be dumped in tree form, with one indent for every new
    control flow block
    """
    result = _parse_arguments()
    do_print(result.filename[0])
