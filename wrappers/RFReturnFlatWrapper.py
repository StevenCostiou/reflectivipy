import ast
from .RFFlatWrapper import RFFlatWrapper


class RFReturnFlatWrapper(RFFlatWrapper):
    def __init__(self, rf_node):
        super(RFReturnFlatWrapper, self).__init__(rf_node)
        self.additional_after_links = []

    def transform_node(self):
        value_assign = self.builder.assign_named_value(self.original_node.temp_name, self.original_node.value)
        self.node_transformation.append(self.builder.build_rf_node(value_assign))

    def basic_wrap(self):
        super(RFReturnFlatWrapper, self).basic_wrap()
        self.append_links(self.additional_after_links)
        return_node = ast.Return(self.builder.ast_load(self.original_node.temp_name))
        self.body.append(self.builder.build_rf_node(return_node))
        return self.body

    def should_wrap(self, rf_node):
        return super(RFReturnFlatWrapper, self).should_wrap(rf_node) \
               or self.additional_after_links
