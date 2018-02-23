import inspect
import ast
from wrappers import flat_wrappers
# Extends the PyPy ast with Reflectivity attributes.
# The base node is a MethodNode (for every function or method).


class RFAstBuilder:
    def __init__(self):
        self.method_node = None
        self.current_index = 1

    def assign_named_value(self, name, value):
        value_store = self.ast_store(name)
        value_assign = self.ast_assign(value_store, value)
        return self.build_rf_node(value_assign)

    def ast_assign(self, store_node, value_node):
        return ast.Assign(targets=[store_node], value=value_node)

    def ast_store(self, var_name):
        return ast.Name(id=var_name, ctx=ast.Store())

    def ast_load(self, var_name):
        return ast.Name(id=var_name, ctx=ast.Load())

    def get_method_source(self, method):
        lines = inspect.getsourcelines(method)
        src = ''
        for line in lines[0]:
            src += line[4:]
        return src

    def ast_for_method(self, method):
        return ast.parse(self.get_method_source(method))

    def rf_ast_for_method(self, method_class, method, method_name):
        method_node = self.ast_for_method(method)
        method_node.method_name = method_name
        method_node.method_class = method_class
        return self.build_rf_ast(method_node)

    def build_rf_ast(self, node):
        self.method_node = node
        self.method_node.is_method = True
        self.visit_node(self.method_node)
        return node

    def visit_node(self, node):
        self.decorate_node(node)

        for child in ast.iter_child_nodes(node):
            child.parent = node
            node.children.append(child)
            self.visit_node(child)

        return node

    def build_rf_node(self, node):
        self.decorate_node(node)
        return self.decorate_node(node)

    def decorate_node(self, node):
        if not node == self.method_node:
            node.is_method = False

        node.method_node = self.method_node
        node.wrapping_method_node = self.method_node

        node.rf_id = self.current_index
        self.current_index += 1

        node.method_class = self.method_node.method_class
        node.links = set()

        if node.__class__ in flat_wrappers:
            node.wrapper = flat_wrappers[node.__class__](node)
        else:
            node.wrapper = flat_wrappers['generic'](node)

        node.children = list()
        return node
