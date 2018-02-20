import copy

from wrappers.RFNodeWrapper import *


class RFMethodNodeWrapper(RFNodeWrapper):
    def basic_wrap(self, rf_method_node):
        rf_method = rf_method_node.reflective_method

        args = []
        for arg in rf_method_node.body[0].args.args:
            if not arg.id == 'self':
                args.append(arg)

        call_node = self.generate_call_to_wrapped(rf_method.wrapped_method_name(), args)
        return ast_assign(self.store_node_for_return(), call_node)

    def base_wrapper_node_from(self, rf_method):
        return rf_method.new_method_wrapper_node()

    def replace_node_by_wrapper(self, rf_node, wrapper_node):
        wrapped_ast = self.build_wrapped_ast(rf_node)
        self.compile_wrapper_node(wrapped_ast)

        rf_node.reflective_method.wrapping_ast = wrapper_node
        rf_node.reflective_method.wrapped_ast = wrapped_ast

    def build_wrapped_ast(self, rf_method_node):
        wrapped_ast = copy.copy(rf_method_node)

        func_def_node = wrapped_ast.body[0]
        func_def_node.name = rf_method_node.reflective_method.wrapped_method_name()

        ast.fix_missing_locations(wrapped_ast)
        return wrapped_ast
