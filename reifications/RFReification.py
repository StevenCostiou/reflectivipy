import ast


class RFReification(object):
    def visit_node(self, rf_node):
        return self.visit_method(rf_node)(rf_node)

    def visit_method(self, rf_node):
        visit_method = 'visit_' + rf_node.__class__.__name__
        return getattr(self, visit_method)


class RFConstReification(RFReification, object):
    def __init__(self, value):
        self.value = value

    def visit_node(self, rf_node):
        return ast.Const(self.value)


class RFClassReification(RFReification, object):
    def visit_node(self, rf_node):
        return RFConstReification(rf_node.method_class).visit_node(rf_node)


class RFObjectReification(RFReification, object):
    def visit_node(self, rf_node):
        return ast.Name(id='self', ctx=ast.Load())


class RFNodeReification(RFReification, object):
    def visit_node(self, rf_node):
        return RFConstReification(rf_node).visit_node(rf_node)


class RFMethodReification(RFReification, object):
    def visit_node(self, rf_node):
        method = rf_node.method_node.reflective_method.target_entity
        method_name = rf_node.method_node.method_name
        return RFConstReification(getattr(method, method_name)).visit_node(rf_node)


class RFSenderReification(RFReification, object):
    def visit_node(self, rf_node):
        method_name = rf_node.method_node.method_name
        return RFConstReification(method_name).visit_node(rf_node)


class RFReceiverReification(RFReification, object):
    def visit_node(self, rf_node):
        return ast.Name(id=rf_node.func.value.temp_name, ctx=ast.Load())


class RFSelectorReification(RFReification, object):
    def visit_node(self, rf_node):
        return ast.Str(rf_node.func.attr)


class RFValueReification(RFReification, object):
    def visit_Assign(self, assign_node):
        return ast.Name(id=assign_node.targets[0].id, ctx=ast.Load())

    def visit_Name(self, name):
        return name


class RFOldValueReification(RFValueReification, object):
    def visit_Assign(self, assign_node):
        return ast.Name(id=assign_node.targets[0].id, ctx=ast.Load())


class RFNewValueReification(RFValueReification, object):
    def visit_Assign(self, assign_node):
        return ast.Name(id=assign_node.temp_name, ctx=ast.Load())


class RFNameReification(RFReification, object):
    def visit_Assign(self, assign_node):
        return self.visit_Name(assign_node.targets[0])

    def visit_Name(self, name_node):
        return ast.Str(name_node.id)


class RFArgumentReification(RFReification, object):
    def visit_Module(self, rf_node):
        return self.visit_FunctionDef(rf_node.body[0])

    def visit_FunctionDef(self, rf_node):
        args = list()
        for arg in rf_node.args.args:
            if not arg.id == 'self':
                args.append(ast.Name(id=arg.id, ctx=ast.Load()))

        return ast.List(elts=args, ctx=ast.Load())

    def visit_Call(self, rf_node):
        args = list()
        for arg in rf_node.args:
            args.append(ast.Name(id=arg.id, ctx=ast.Load()))

        return ast.List(elts=args, ctx=ast.Load())


reifications = dict()
reifications['class'] = RFClassReification
reifications['node'] = RFNodeReification
reifications['object'] = RFObjectReification
reifications['method'] = RFMethodReification
reifications['sender'] = RFSenderReification
reifications['receiver'] = RFReceiverReification
reifications['selector'] = RFSelectorReification
reifications['name'] = RFNameReification
reifications['value'] = RFValueReification
reifications['old_value'] = RFOldValueReification
reifications['new_value'] = RFNewValueReification
reifications['arguments'] = RFArgumentReification


def reification_for(key, metalink):
    if key in reifications:
        return reifications[key]()
    if key == 'link':
        return RFConstReification(metalink)
    return RFConstReification(key)
