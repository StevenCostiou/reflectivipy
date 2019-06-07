import ast
from ..core import AstBuilder
from ..reifications import ReificationGenerator, link_reification


class FlatWrapper(object):
    def __init__(self, rf_node):
        self.body = []
        self.preambles = []
        self.flattened_children = []
        self.before_links = []
        self.after_links = []
        self.instead_links = []
        self.original_node = rf_node
        self.reifications = set()
        self.node_transformation = []
        self.builder = AstBuilder()
        self.builder.method_node = self.original_node.method_node
        self.reifyer = ReificationGenerator()

    def reset_wrapping(self):
        self.body = []
        self.preambles = []
        self.flattened_children = []
        self.before_links = []
        self.after_links = []
        self.instead_links = []
        self.node_transformation = []

    def gen_preambles(self):
        preambles = self.reifyer.generate_reifications(self.original_node)
        self.preambles.extend(preambles)

    def flatten_children(self):
        pass

    def transform_node(self):
        self.node_transformation.append(self.original_node)

    def gen_link_node(self, link):
        arguments = []
        arguments.extend(link.reified_arguments)

        metaobject_node = ast.Attribute(
            value=link_reification(link), attr="metaobject", ctx=ast.Load()
        )
        attr_node = ast.Attribute(
            value=metaobject_node, attr=link.selector, ctx=ast.Load()
        )
        call_node = ast.Call(func=attr_node, args=arguments, keywords=[])

        return ast.Expr(call_node)

    def sort_links(self):
        for link in self.original_node.links:
            if link.control == "before":
                self.before_links.append(link)
            if link.control == "after":
                self.after_links.append(link)
            if link.control == "instead":
                self.instead_links.append(link)

    def flat_wrap(self):
        self.reset_wrapping()
        self.gen_preambles()
        self.sort_links()

        if not self.should_wrap(self.original_node):
            self.body.append(self.original_node)
            return self.body

        self.init_wrapping()
        return self.basic_wrap()

    def init_wrapping(self):
        self.flatten_children()
        self.transform_node()

    def basic_wrap(self):
        self.append_flattened_children()
        self.append_preambles()
        self.append_links(self.before_links)
        self.append_node_transformation()
        self.append_links(self.after_links)
        return self.body

    def should_wrap(self, rf_node):
        return self.should_wrap_node(rf_node) or self.should_wrap_children(rf_node)

    def should_wrap_node(self, rf_node):
        if rf_node.links:
            return True
        return False

    def should_wrap_children(self, rf_node):
        for node in rf_node.children:
            if self.should_wrap(node):
                return True
        return False

    def append_preambles(self):
        for node in self.preambles:
            self.body.append(node)

    def append_flattened_children(self):
        for node in self.flattened_children:
            if hasattr(node, "wrapper"):
                self.body.extend(node.wrapper.flat_wrap())
            else:
                self.body.append(node)

    def append_node_transformation(self):
        if self.instead_links:
            self.body.append(self.gen_link_node(self.instead_links[0]))
            return

        for node in self.node_transformation:
            self.body.append(node)

    def append_links(self, links):
        for link in links:
            self.body.append(self.gen_link_node(link))
