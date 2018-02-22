# Extends the PyPy ast with Reflectivity attributes.
# The base node is a MethodNode (for every function or method).

import Reflectivity
from ast_tools import *


class RFAstBuilder:
    def __init__(self):
        self.method_node = None
        self.current_index = 1

    def rf_ast_for_method(self, method_class, method, method_name):
        method_node = ast_for_method(method)
        method_node.method_name = method_name
        method_node.method_class = method_class
        return self.build_rf_ast(method_node)

    def build_rf_ast(self, node):
        self.method_node = node
        self.method_node.is_method = True
        self.visit_node(self.method_node)
        return node

    def visit_node(self, node):
        if not node == self.method_node:
            node.is_method = False

        node.method_node = self.method_node
        node.wrapping_method_node = self.method_node

        node.rf_id = self.current_index
        self.current_index += 1

        node.method_class = self.method_node.method_class
        node.links = set()

        if node.__class__ in Reflectivity.flat_wrappers:
            node.wrapper = Reflectivity.flat_wrappers[node.__class__](node)
        else:
            node.wrapper = Reflectivity.flat_wrappers['generic'](node)

        children = []

        for child in ast.iter_child_nodes(node):
            child.parent = node
            children.append(child)
            self.visit_node(child)

        node.children = children
        return node
