import ast
from .core import AstBuilder

builder = AstBuilder()


class Reification(object):
    def visit_node(self, rf_node, metalink):
        return self.visit_method(rf_node)(rf_node, metalink)

    def visit_method(self, rf_node):
        visit_method = "visit_" + rf_node.__class__.__name__
        return getattr(self, visit_method)


class LiteralValueReification(Reification):
    def __init__(self, value):
        self.value = value

    def visit_node(self, rf_node, metalink):
        rf_node.method_node.reflective_method.add_literal_value_reification(self.value)
        attr_node = ast.Attribute(
            value=rf_method_reification(),
            attr="get_literal_value_reifications",
            ctx=ast.Load(),
        )
        return ast.Call(func=attr_node, args=[ast.Num(id(self.value))], keywords=[])


class LinkReification(Reification):
    def visit_node(self, rf_node, metalink):
        return link_reification(metalink)


class ClassReification(Reification):
    def visit_node(self, rf_node, metalink):
        return ast.Attribute(
            value=node_reification(), attr="method_class", ctx=ast.Load()
        )


class ObjectReification(Reification):
    def visit_node(self, rf_node, metalink):
        return ast.Name(id="self", ctx=ast.Load())


class NodeReification(Reification):
    def visit_node(self, rf_node, metalink):
        attr_node = ast.Attribute(
            value=rf_method_reification(),
            attr="find_node_of_id_in_link",
            ctx=ast.Load(),
        )
        return ast.Call(
            func=attr_node,
            args=[ast.Num(rf_node.rf_id), link_reification(metalink)],
            keywords=[],
        )


class MethodReification(Reification):
    def visit_node(self, rf_node, metalink):
        return original_method_reification()


class SenderReification(Reification):
    def visit_node(self, rf_node, metalink):
        method_node_node = ast.Attribute(
            value=node_reification(), attr="method_node", ctx=ast.Load()
        )
        return ast.Attribute(value=method_node_node, attr="method_name", ctx=ast.Load())


class ReceiverReification(Reification):
    def visit_node(self, rf_node, metalink):
        return ast.Name(id=rf_node.func.value.temp_name, ctx=ast.Load())


class SelectorReification(Reification):
    def visit_node(self, rf_node, metalink):
        return ast.Str(rf_node.func.attr)


class ValueReification(Reification):
    def visit_Assign(self, assign_node, metalink):
        return ast.Name(id=assign_node.targets[0].id, ctx=ast.Load())

    def visit_Name(self, name, metalink):
        return name


class OldValueReification(ValueReification):
    def visit_Assign(self, assign_node, metalink):
        return ast.Name(id=assign_node.targets[0].id, ctx=ast.Load())


class NewValueReification(ValueReification):
    def visit_Assign(self, assign_node, metalink):
        return ast.Name(id=assign_node.temp_name, ctx=ast.Load())


class NameReification(Reification):
    def visit_Assign(self, assign_node, metalink):
        return self.visit_Name(assign_node.targets[0], metalink)

    def visit_Name(self, name_node, metalink):
        return ast.Str(name_node.id)


class ArgumentReification(Reification):
    def visit_Module(self, rf_node, metalink):
        return self.visit_FunctionDef(rf_node.body[0], metalink)

    def visit_FunctionDef(self, rf_node, metalink):
        args = []
        for arg in rf_node.args.args:
            if not arg.arg == "self":
                args.append(ast.Name(id=arg.arg, ctx=ast.Load()))

        return ast.List(elts=args, ctx=ast.Load())

    def visit_Call(self, rf_node, metalink):
        args = []
        for arg in rf_node.args:
            args.append(ast.Name(id=arg.id, ctx=ast.Load()))

        return ast.List(elts=args, ctx=ast.Load())


reifications_dict = {
    "class": ClassReification,
    "node": NodeReification,
    "object": ObjectReification,
    "method": MethodReification,
    "sender": SenderReification,
    "receiver": ReceiverReification,
    "selector": SelectorReification,
    "name": NameReification,
    "value": ValueReification,
    "old_value": OldValueReification,
    "new_value": NewValueReification,
    "arguments": ArgumentReification,
    "link": LinkReification,
}


def reification_for(key, metalink):
    if key in reifications_dict:
        return reifications_dict[key]()
    return LiteralValueReification(key)


def rf_method_reification():
    return builder.ast_load("__rf_method__")


def link_reification(link):
    link_id_node = ast.Num(id(link))

    link_attr_node = ast.Attribute(
        value=rf_method_reification(), attr="lookup_link", ctx=ast.Load()
    )
    return ast.Call(func=link_attr_node, args=[link_id_node], keywords=[])


def node_reification():
    return ast.Attribute(
        value=rf_method_reification(), attr="reflective_ast", ctx=ast.Load()
    )


def original_method_reification():
    return ast.Attribute(
        value=rf_method_reification(), attr="original_method", ctx=ast.Load()
    )


class ReificationGenerator(object):
    def __init__(self):
        self.reification_counter = 0
        self.arg_list = []

    def generate_reifications(self, rf_node):
        expressions = []

        for link in rf_node.links:
            link.reset_reified_arguments()

            for arg in link.arguments:
                reification = reification_for(arg, link).visit_node(rf_node, link)
                rf_name = self.rf_name_for_arg(arg, str(rf_node.rf_id))
                expressions.append(builder.assign_named_value(rf_name, reification))
                self.add_reified_argument_to_link(builder.ast_load(rf_name), link)

            if link.option_arg_as_array:
                link.reified_arguments.append(builder.ast_load_list(self.arg_list))
                self.arg_list = []

        return expressions

    def add_reified_argument_to_link(self, arg_node, metalink):
        if metalink.option_arg_as_array:
            self.arg_list.append(arg_node)
        else:
            metalink.reified_arguments.append(arg_node)

    def rf_name_for_arg(self, arg, rf_id):
        if isinstance(arg, str):
            return arg + "_" + rf_id

        self.reification_counter += 1
        return "value_{}_{}".format(rf_id, self.reification_counter)
