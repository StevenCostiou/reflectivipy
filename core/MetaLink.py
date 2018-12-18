class MetaLink:
    def __init__(self, metaobject, selector, control, args):
        self.metaobject = metaobject
        self.selector = selector
        self.control = control
        self.nodes = []
        self.arguments = args
        self.reified_arguments = []
        self.option_arg_as_array = False

    def add_node(self, rf_node):
        self.nodes.append(rf_node)

    def remove_node(self, rf_node):
        self.nodes.remove(rf_node)
        rf_node.links.remove(self)

    def reset_reified_arguments(self):
        self.reified_arguments = []

    def set_args_as_array(self, a_bool):
        self.option_arg_as_array = a_bool
