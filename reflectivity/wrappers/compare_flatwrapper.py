from .flatwrapper import FlatWrapper


class CompareFlatWrapper(FlatWrapper):
    def transform_node(self):
        # TODO : node transformation here
        self.original_node.twin.left = self.builder.ast_load(
            self.original_node.left.temp_name
        )

        comparators = []

        for node in self.original_node.comparators:
            comparators.append(self.builder.ast_load(node.temp_name))
        # TODO : node transformation here
        self.original_node.twin.comparators = comparators

    def flatten_children(self):
        left = self.original_node.left
        self.flattened_children.extend(left.wrapper.flat_wrap())

        for node in self.original_node.comparators:
            self.flattened_children.extend(node.wrapper.flat_wrap())
