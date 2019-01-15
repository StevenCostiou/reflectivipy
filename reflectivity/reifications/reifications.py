import ast


class Reification(object):
    def visit_node(self, rf_node):
        return self.visit_method(rf_node)(rf_node)

    def visit_method(self, rf_node):
        visit_method = 'visit_' + rf_node.__class__.__name__
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
        return ast.Name(id='self', ctx=ast.Load())


class NodeReification(Reification):
    def visit_node(self, rf_node):
        return ConstReification(rf_node).visit_node(rf_node)


class MethodReification(Reification):
    def visit_node(self, rf_node):
        method = rf_node.method_node.reflective_method.target_entity
        method_name = rf_node.method_node.method_name
        return ConstReification(getattr(method, method_name)).visit_node(rf_node)


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
            if not arg.id == 'self':
                args.append(ast.Name(id=arg.id, ctx=ast.Load()))

        return ast.List(elts=args, ctx=ast.Load())

    def visit_Call(self, rf_node):
        args = []
        for arg in rf_node.args:
            args.append(ast.Name(id=arg.id, ctx=ast.Load()))

        return ast.List(elts=args, ctx=ast.Load())
