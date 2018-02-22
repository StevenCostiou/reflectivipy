from core import ast_tools as rf_ast


class RFFlatWrapper:
    def __init__(self, rf_node):
        self.body = list()
        self.preambles = list()
        self.flattened_children = list()
        self.before_links = list()
        self.after_links = list()
        self.instead_links = list()
        self.original_node = rf_node
        self.reifications = set()
        self.node_transformation = list()

    def reset_wrapping(self):
        self.body = list()
        self.preambles = list()
        self.flattened_children = list()
        self.before_links = list()
        self.after_links = list()
        self.instead_links = list()
        self.node_transformation = list()

    def gen_preambles(self):
        for link in self.original_node.links:
            self.gen_reifications(link)

    def gen_reifications(self, link):
        pass

    def flatten_children(self):
        pass

    def transform_node(self):
        self.node_transformation.append(self.original_node)

    def gen_link_node(self, link):
        metaobject = link.metaobject
        selector = link.selector

        arguments = list()
        for arg in link.arguments:
            arguments.append(rf_ast.ast_load(arg))

        metaobject_node = rf_ast.Const(metaobject)
        attr_node = rf_ast.Attribute(value=metaobject_node, attr=selector, ctx=rf_ast.Load())
        call_node = rf_ast.Call(func=attr_node, args=arguments, keywords=[])

        return rf_ast.Expr(call_node)

    def sort_links(self):
        for link in self.original_node.links:
            if link.control == 'before':
                self.before_links.append(link)
            if link.control == 'after':
                self.after_links.append(link)
            if link.control == 'instead':
                self.instead_links.append(link)

    def flat_wrap(self):
        self.reset_wrapping()
        self.sort_links()

        if not self.should_wrap(self.original_node):
            self.body.append(self.original_node)
            return self.body

        self.init_wrapping()
        return self.basic_wrap()

    def init_wrapping(self):
        self.flatten_children()
        self.transform_node()
        self.gen_preambles()

    def basic_wrap(self):
        self.append_flattened_children()
        self.append_preambles()
        self.append_links(self.before_links)
        self.append_node_transformation()
        self.append_links(self.after_links)
        return self.body

    def should_wrap(self, rf_node):
        if rf_node.links:
            return True

        for node in rf_node.children:
            if self.should_wrap(node):
                return True

        return False

    def append_preambles(self):
        for node in self.preambles:
            self.body.append(node)

    def append_flattened_children(self):
        for node in self.flattened_children:
            if hasattr(node, 'wrapper'):
                self.body.extend(node.wrapper.flat_wrap())
            else:
                self.body.append(node)

    def append_node_transformation(self):
        if self.instead_links:
            self.body.append(self.instead_links.reverse()[0])
            return

        for node in self.node_transformation:
            self.body.append(node)

    def append_links(self, links):
        for link in links:
            self.body.append(self.gen_link_node(link))