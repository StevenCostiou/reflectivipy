'''
Extends the PyPy ast with Reflectivity attributes.
The base node is a MethodNode (for every function or method).

What is added:
- methodNode accessor
- parent
- type checking
- name accessor
- id

'''
from Hook import Hook
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

    def rf_ast(self, method):
        method_node = ast_for_method(method)
        method_node.method_name = method.__name__
        method_node.method_class = method.__class__
        return self.build_rf_ast(method_node)

    def build_rf_ast(self, ast):
        self.method_node = ast
        self.method_node.is_method = True
        self.visit_node(self.method_node)
        return ast

    def visit_node(self, node):
        if not node == self.method_node:
            node.is_method = False

        self.set_method_node(node)
        self.set_index(node)
        self.set_hook(node)
        node.method_class = self.method_node.method_class

        children = []

        for child in ast.iter_child_nodes(node):
            child.parent = node
            children.append(child)
            self.visit_node(child)

        self.set_children(node, children)
        return node

    def set_method_node(self, node):
        node.method_node = self.method_node
        node.wrapping_method_node = self.method_node

    def set_index(self, node):
        node.rf_id = self.current_index
        self.current_index += 1

    def set_children(self, node, children):
        node.children = children

    def set_hook(self, node):
        node.hook = Hook()
