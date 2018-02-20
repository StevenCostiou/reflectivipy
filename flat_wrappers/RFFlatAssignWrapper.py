from RFFlatWrapper import rf_ast
from RFFlatWrapper import RFFlatWrapper


class RFFlatAssignWrapper(RFFlatWrapper):
    def flatten_children(self):
        value_store = rf_ast.ast_store('value')
        value_assign = rf_ast.ast_assign(value_store, self.transformed_node.value)

        self.flattened_children.append(value_assign)

        self.transformed_node.value = rf_ast.ast_load('value')
