import ast
from RFFlatWrapper import RFFlatWrapper


class RFAssignFlatWrapper(RFFlatWrapper):
    def flatten_children(self):
        value_assign = self.builder.assign_named_value(self.reify_name('value'), self.original_node.value)
        self.flattened_children.append(value_assign)

    def transform_node(self):
        targets = self.original_node.targets
        value = self.builder.ast_load(self.reify_name('value'))
        transformed_assign = ast.Assign(targets=targets, value=value)
        self.node_transformation.append(transformed_assign)
