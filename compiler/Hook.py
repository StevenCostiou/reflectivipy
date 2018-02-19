import ast


class Hook:
    def __init__(self):
        self.after_links = set()
        self.before_links = set()
        self.instead_links = set()
        self.inactive_instead_links = set()
        self.inactive_after_links = set()
        self.inactive_before_links = set()

    def exec_before_links(self, reifications):
        print("before links executing...")
        for link in self.before_links:
            link.exec_link(link, reifications)

    def exec_after_links(self, reifications):
        print("after links executing...")
        for link in self.after_links:
            link.exec_link(link, reifications)

    def activate_link(self, link):
        pass

    def deactivate_link(self, link):
        pass

    def gen_call_node(self, selector, reifications):
        args = list()
        args.append(reifications)
        attr_node = ast.Attribute(value=ast.Const(self), attr=selector, ctx=ast.Load())
        call_node = ast.Call(func=attr_node, args=args, keywords=[])
        return ast.Expr(call_node)

    def gen_before_call_node(self, reifications):
        return self.gen_call_node('exec_before_links', reifications)

    def gen_after_call_node(self, reifications):
        return self.gen_call_node('exec_after_links', reifications)

    def add_link_before(self, metalink):
        self.before_links.add(metalink)

    def add_link_after(self, metalink):
        self.after_links.add(metalink)

    def add_link_instead(self, metalink):
        self.instead_links.add(metalink)
