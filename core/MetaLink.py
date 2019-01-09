class MetaLink(object):
    def __init__(self, metaobject, selector, control='before', arguments=None):
        self.metaobject = metaobject
        self.selector = selector
        self.control = control
        self.nodes = []
        self.arguments = arguments or []
        self.reified_arguments = []
        self.option_arg_as_array = False

    def add_node(self, rf_node):
        self.nodes.append(rf_node)

    def remove_node(self, rf_node):
        self.nodes.remove(rf_node)
        rf_node.links.remove(self)

    def uninstall(self, from_node=None):
        nodes = [from_node] if from_node else list(self.nodes)
        for node in nodes:
            self.remove_node(node)

    def reset_reified_arguments(self):
        self.reified_arguments = []
