from compiler import ast_tools as rf_ast


class RFFlatWrapper:
    def __init__(self, rf_node):
        self.body = list()
        self.preambles = list()
        self.flattened_children = list()
        self.before_links = list()
        self.after_links = list()
        self.instead_links = list()
        self.transformed_node = rf_node
        self.reifications = set()

    def reset_wrapping(self):
        self.body = list()
        self.preambles = list()
        self.flattened_children = list()
        self.before_links = list()
        self.after_links = list()
        self.instead_links = list()

    def gen_preambles(self):
        for link in self.transformed_node.links:
            self.gen_reifications(link)

    def gen_reifications(self, link):
        pass

    def flatten_children(self):
        pass

    def gen_link_node(self, link):
        metaobject = link.metaobject
        selector = link.selector
        arguments = list()
        for arg in link.args:
            arguments.append(rf_ast.ast_load(arg))

        metaobject_node = rf_ast.Const(metaobject)
        attr_node = rf_ast.Attribute(value=metaobject_node, attr=selector, ctx=rf_ast.Load())

        call_node = rf_ast.Call(func=attr_node, args=arguments, keywords=[])

        return rf_ast.Expr(call_node)

    def sort_links(self):
        for link in self.transformed_node.links:
            if link.control == 'before':
                self.before_links.append(link)
            if link.control == 'after':
                self.after_links.append(link)
            if link.control == 'instead':
                self.instead_links.append(link)

    def flat_wrap(self):
        if self.should_wrap(self.transformed_node):
            return self.basic_wrap()

        self.body.append(self.transformed_node)
        return self.body

    def basic_wrap(self):
        self.reset_wrapping()
        self.sort_links()
        self.flatten_children()
        self.gen_preambles()

        for node in self.flattened_children:
            if hasattr(node, 'wrapper'):
                self.body.extend(node.wrapper.flat_wrap())
            else:
                self.body.append(node)

        for node in self.preambles:
            self.body.append(node)

        for link in self.before_links:
            self.body.append(self.gen_link_node(link))

        if len(self.instead_links) > 0:
            self.body.append(self.instead_links.reverse()[0])
        else:
            self.body.append(self.transformed_node)

        for link in self.after_links:
            self.body.append(self.gen_link_node(link))

        return self.body

    def should_wrap(self, rf_node):
        if rf_node.links:
            return True

        for node in rf_node.children:
            if self.should_wrap(node):
                return True

        return False
