import ast
from .flatwrapper import FlatWrapper


class AssignFlatWrapper(FlatWrapper):
    def flatten_children(self):
        value_node = self.original_node.value

        if self.is_node_call_with_links(value_node):
            self.flattened_children.append(value_node)
            return

        value_assign = self.builder.assign_named_value(
            self.original_node.temp_name, value_node
        )
        rf_assign = self.builder.build_rf_node(value_assign)
        self.flattened_children.append(rf_assign)

    def transform_node(self):
        if self.original_node.is_generated:
            self.node_transformation.append(self.original_node)
            return

        targets = self.original_node.targets
        value_node = self.original_node.value
        temp_name = self.original_node.temp_name
        if self.is_node_call_with_links(value_node):
            temp_name = value_node.temp_name
        value = self.builder.ast_load(temp_name)
        transformed_assign = ast.Assign(targets=targets, value=value)
        self.node_transformation.append(transformed_assign)

    def is_node_call_with_links(self, rf_node):
        if rf_node.__class__ is not ast.Call:
            return False
        return rf_node.wrapper.should_wrap(rf_node)
