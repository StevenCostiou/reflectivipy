from wrappers.RFNodeWrapper import *


class RFAssignWrapper(RFNodeWrapper):
    def basic_wrap(self, rf_node):
        return gen_ast_assignment(self.store_node_for_return(), rf_node.value)

    def replace_node_by_wrapper(self, rf_node, wrapper_node):
        rf_node.value = self.wrapper_call_node(wrapper_node)
        parent_method_node = rf_node.method_node.reflective_method.wrapped_ast
        ast.fix_missing_locations(parent_method_node)
