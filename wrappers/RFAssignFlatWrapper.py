from RFFlatWrapper import rf_ast
from RFFlatWrapper import RFFlatWrapper


class RFAssignFlatWrapper(RFFlatWrapper):
    def flatten_children(self):
        value_store = rf_ast.ast_store('value')
        value_assign = rf_ast.ast_assign(value_store, self.original_node.value)
        self.flattened_children.append(value_assign)

    def transform_node(self):
        targets = self.original_node.targets
        value = rf_ast.ast_load('value')
        transformed_assign = rf_ast.Assign(targets=targets, value=value)
        self.node_transformation.append(transformed_assign)
