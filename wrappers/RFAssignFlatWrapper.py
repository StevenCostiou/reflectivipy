import ast
from RFFlatWrapper import RFFlatWrapper


class RFAssignFlatWrapper(RFFlatWrapper):
    def flatten_children(self):
        value_assign = self.builder.assign_named_value(self.original_node.temp_name, self.original_node.value)
        self.flattened_children.append(self.builder.build_rf_node(value_assign))

    def transform_node(self):
        targets = self.original_node.targets
        value = self.builder.ast_load(self.original_node.temp_name)
        transformed_assign = ast.Assign(targets=targets, value=value)
        self.node_transformation.append(transformed_assign)
