import ast
from .core import AstBuilder


class Reification(object):
    def visit_node(self, rf_node):
        return self.visit_method(rf_node)(rf_node)

    def visit_method(self, rf_node):
        visit_method = "visit_" + rf_node.__class__.__name__
        return getattr(self, visit_method)


class ConstReification(Reification):
    def __init__(self, value):
        self.value = value

    def visit_node(self, rf_node):
        return ast.Const(self.value)


class ClassReification(Reification):
    def visit_node(self, rf_node):
        return ConstReification(rf_node.method_class).visit_node(rf_node)


class ObjectReification(Reification):
    def visit_node(self, rf_node):
        return ast.Name(id="self", ctx=ast.Load())


class NodeReification(Reification):
    def visit_node(self, rf_node):
        return ConstReification(rf_node).visit_node(rf_node)


class MethodReification(Reification):
    def visit_node(self, rf_node):
        method = rf_node.method_node.reflective_method.target_entity
        method_name = rf_node.method_node.method_name
        method_attr = getattr(method, method_name)
        return ConstReification(method_attr).visit_node(rf_node)


class SenderReification(Reification):
    def visit_node(self, rf_node):
        method_name = rf_node.method_node.method_name
        return ConstReification(method_name).visit_node(rf_node)


class ReceiverReification(Reification):
    def visit_node(self, rf_node):
        return ast.Name(id=rf_node.func.value.temp_name, ctx=ast.Load())


class SelectorReification(Reification):
    def visit_node(self, rf_node):
        return ast.Str(rf_node.func.attr)


class ValueReification(Reification):
    def visit_Assign(self, assign_node):
        return ast.Name(id=assign_node.targets[0].id, ctx=ast.Load())

    def visit_Name(self, name):
        return name


class OldValueReification(ValueReification):
    def visit_Assign(self, assign_node):
        return ast.Name(id=assign_node.targets[0].id, ctx=ast.Load())


class NewValueReification(ValueReification):
    def visit_Assign(self, assign_node):
        return ast.Name(id=assign_node.temp_name, ctx=ast.Load())


class NameReification(Reification):
    def visit_Assign(self, assign_node):
        return self.visit_Name(assign_node.targets[0])

    def visit_Name(self, name_node):
        return ast.Str(name_node.id)


class ArgumentReification(Reification):
    def visit_Module(self, rf_node):
        return self.visit_FunctionDef(rf_node.body[0])

    def visit_FunctionDef(self, rf_node):
        args = []
        for arg in rf_node.args.args:
            if not arg.id == "self":
                args.append(ast.Name(id=arg.id, ctx=ast.Load()))

        return ast.List(elts=args, ctx=ast.Load())

    def visit_Call(self, rf_node):
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
}


def reification_for(key, metalink):
    if key in reifications_dict:
        return reifications_dict[key]()
    if key == "link":
        return ConstReification(metalink)
    return ConstReification(key)


class ReificationGenerator(object):
    def __init__(self):
        self.builder = AstBuilder()
        self.reification_counter = 0
        self.arg_list = []

    def generate_reifications(self, rf_node):
        expressions = []

        for link in rf_node.links:
            link.reset_reified_arguments()

            for arg in link.arguments:
                reification = reification_for(arg, link).visit_node(rf_node)
                rf_name = self.rf_name_for_arg(arg, str(rf_node.rf_id))
                expressions.append(
                    self.builder.assign_named_value(rf_name, reification)
                )
                self.add_reified_argument_to_link(self.builder.ast_load(rf_name), link)

            if link.option_arg_as_array:
                link.reified_arguments.append(self.builder.ast_load_list(self.arg_list))
                self.arg_list = []

        return expressions

    def add_reified_argument_to_link(self, arg_node, metalink):
        if metalink.option_arg_as_array:
            self.arg_list.append(arg_node)
        else:
            metalink.reified_arguments.append(arg_node)

    def rf_name_for_arg(self, arg, rf_id):
        if isinstance(arg, basestring):
            return arg + "_" + rf_id

        self.reification_counter += 1
        return "value_{}_{}".format(rf_id, self.reification_counter)
