import ast
from .flatwrapper import FlatWrapper


class ReturnFlatWrapper(FlatWrapper):
    def __init__(self, rf_node):
        super(ReturnFlatWrapper, self).__init__(rf_node)
        self.additional_after_links = []

    def transform_node(self):
        original_node = self.original_node
        builder = self.builder
        value_assign = builder.assign_named_value(
            original_node.temp_name, original_node.value
        )
        self.node_transformation.append(builder.build_rf_node(value_assign))

    def basic_wrap(self):
        super(ReturnFlatWrapper, self).basic_wrap()
        self.append_links(self.additional_after_links)
        builder = self.builder
        return_node = ast.Return(builder.ast_load(self.original_node.temp_name))
        self.body.append(builder.build_rf_node(return_node))
        return self.body

    def should_wrap(self, rf_node):
        return (
            super(ReturnFlatWrapper, self).should_wrap(rf_node)
            or self.additional_after_links
        )
