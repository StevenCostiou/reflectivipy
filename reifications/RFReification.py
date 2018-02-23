import ast


class RFReification(object):
    def visit_node(self, rf_node):
        pass


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
        return RFConstReification(rf_node.method_node.method_name).visit_node(rf_node)


reifications = dict()
reifications['class'] = RFClassReification
reifications['node'] = RFNodeReification
reifications['object'] = RFObjectReification
reifications['method'] = RFClassReification

reifications['name'] = RFClassReification
reifications['receiver'] = RFClassReification
reifications['sender'] = RFClassReification
reifications['arguments'] = RFClassReification
reifications['selector'] = RFClassReification
reifications['value'] = RFClassReification


def reification_for(key, metalink):
    if key in reifications:
        return reifications[key]
    if key == 'link':
        return RFConstReification(metalink)
    return RFConstReification(key)
