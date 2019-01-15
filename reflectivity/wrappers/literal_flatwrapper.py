from .flatwrapper import FlatWrapper


class LiteralFlatWrapper(FlatWrapper):
    def transform_node(self):
        assign = self.builder.assign_named_value(
            self.original_node.temp_name, self.original_node
        )
        self.node_transformation.append(self.builder.build_rf_node(assign))

    def should_wrap(self, rf_node):
        return True
