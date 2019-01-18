from .flatwrapper import FlatWrapper


class CallFlatWrapper(FlatWrapper):
    def flatten_children(self):
        self.flattened_children.extend(self.original_node.args)
        self.flattened_children.append(self.extract_receiver_node())

    def transform_node(self):
        twin = self.original_node.twin
        new_args = []
        for arg in self.original_node.args:
            new_args.append(self.builder.ast_load(arg.temp_name))

        twin.args = new_args
        twin.func.value = self.builder.ast_load(twin.func.value.temp_name)
        transformed_node = self.builder.assign_named_value(
            self.original_node.temp_name, twin
        )
        self.node_transformation.append(transformed_node)

    def extract_receiver_node(self):
        receiver = self.original_node.func.value

        if receiver.links:
            return receiver

        return self.builder.assign_named_value(receiver.temp_name, receiver)
