import copy

from ast_tools import *


class ReflectiveMethod():
    def __init__(self, original_ast, class_or_object):
        self.target_entity = class_or_object
        self.original_ast = original_ast
        self.original_ast.reflective_method = self
        self.method_name = self.original_ast.body[0].name
        self.wrapped_ast = None
        self.wrapping_ast = None
        self.wrapped_nodes = {}
        self.links = set()
        self.args = []
        self.nb_wrapped_nodes = 0

    ######################################################
    # Linking for methods                                #
    ######################################################

    def link(self, metalink):
        self.links.add(metalink)

    ######################################################
    # Wrapper helpers                                    #
    ######################################################

    def has_wrappers(self):
        return not ((self.wrapping_ast is None) | (self.wrapped_ast is None))

    # Returns the wrapped name of a method
    def wrapped_method_name(self):
        return "wrapped_" + self.method_name

    def wrapper_for_node(self, wrapper_node, rf_node):
        self.wrapped_nodes[rf_node] = wrapper_node

    def is_node_wrapped(self, rf_node):
        return rf_node in self.wrapped_nodes.keys()

    ######################################################
    # Anonymous function nodes for ast node wrapping     #
    ######################################################

    def new_wrapped_node_name(self):
        self.nb_wrapped_nodes = self.nb_wrapped_nodes + 1
        return 'wrapped_func_' + str(self.nb_wrapped_nodes)

    def new_source_for_wrapper_node(self):
        return 'def ' + self.new_wrapped_node_name() + '(self): pass'

    def new_wrapper_node(self):
        source_code = self.new_source_for_wrapper_node()
        return ast.parse(source_code)

    def new_method_wrapper_node(self):
        wrapper_node = copy.deepcopy(self.original_ast)
        wrapper_node.reflective_method = self
        return wrapper_node

    ######################################################
    # Method node compilation                            #
    ######################################################

    def compile_rf_method(self, rf_ast, method_name):
        locs = dict()
        compiled_method = compile(rf_ast, "<ast>", 'exec')
        eval(compiled_method, {}, locs)
        setattr(self.target_entity, method_name, locs[method_name])

    def recompile(self):
        self.compile_rf_method(self.wrapped_ast, self.wrapped_method_name())
        self.compile_rf_method(self.wrapping_ast, self.method_name)
        return
