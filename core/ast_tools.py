import ast
import inspect
from ast import *


def get_method_source(method):
    lines = inspect.getsourcelines(method)
    src = ''
    for line in lines[0]:
        src += line[4:]
    return src


def ast_for_method(method):
    return ast.parse(get_method_source(method))


def ast_assign(store_node, value_node):
    return ast.Assign(targets=[store_node], value=value_node)


def ast_store(var_name):
    return ast.Name(id=var_name, ctx=ast.Store())


def ast_load(var_name):
    return ast.Name(id=var_name, ctx=ast.Load())
