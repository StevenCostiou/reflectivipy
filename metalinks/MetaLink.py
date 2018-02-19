from compiler.ast_tools import *


def before(metaobject, selector):
    return BeforeLink(metaobject, selector)


def after(metaobject, selector):
    return AfterLink(metaobject, selector)


def instead(metaobject, selector):
    return InsteadLink(metaobject, selector)


class MetaLink:
    def __init__(self, metaobject, selector):
        self.metaobject = metaobject
        self.selector = selector
        self.arguments = []
        self.arguments.append(ast.Name(id='reifications', ctx=ast.Load()))
        self.compile()

    def compile(self):
        metaobject_node = ast.Const(self.metaobject)
        attr_node = ast.Attribute(value=metaobject_node, attr=self.selector, ctx=ast.Load())
        call_node = ast.Call(func=attr_node, args=self.arguments, keywords=[])

        new_body = list()
        new_body.append(ast.Expr(call_node))
        exec_ast = ast_for_method(self.exec_link)
        exec_ast.body[0].body = new_body
        ast.fix_missing_locations(exec_ast)
        compile_rf_method(exec_ast, self, 'exec_link')

    # Add args in the compilation
    def exec_link(self, reifications):
        return


class BeforeLink(MetaLink):
    def link_to_hook(self, hook):
        hook.add_link_before(self)


class AfterLink(MetaLink):
    def link_to_hook(self, hook):
        hook.add_link_after(self)


class InsteadLink(MetaLink):
    def link_to_hook(self, hook):
        hook.instead_links(self)
