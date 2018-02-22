class MetaLink:
    def __init__(self, metaobject, selector, control, args):
        self.metaobject = metaobject
        self.selector = selector
        self.control = control
        self.nodes = list()
        self.arguments = args

    def add_node(self, rf_node):
        self.nodes.append(rf_node)

    def remove_node(self, rf_node):
        self.nodes.remove(rf_node)
        rf_node.links.remove(self)
