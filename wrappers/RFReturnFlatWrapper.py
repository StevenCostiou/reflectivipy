import ast
from RFFlatWrapper import RFFlatWrapper


class RFReturnFlatWrapper(RFFlatWrapper, object):
    def __init__(self, rf_node):
        super(RFReturnFlatWrapper, self).__init__(rf_node)
        self.additional_after_links = list()

    def transform_node(self):
        value_assign = self.builder.assign_named_value(self.reify_name('return'), self.original_node.value)
        self.node_transformation.append(value_assign)

    def basic_wrap(self):
        super(RFReturnFlatWrapper, self).basic_wrap()
        self.append_links(self.additional_after_links)
        self.body.append(ast.Return(self.builder.ast_load(self.reify_name('return'))))
        return self.body

    def should_wrap(self, rf_node):
        return super(RFReturnFlatWrapper, self).should_wrap(rf_node) \
               or self.additional_after_links
