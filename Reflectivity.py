from compiler.RFAstBuilder import RFAstBuilder
from compiler.ReflectiveMethod import ReflectiveMethod
from wrappers.RFAssignWrapper import *
from wrappers.RFMethodNodeWrapper import RFMethodNodeWrapper

rf_methods = dict()
wrappers = dict()
wrappers[ast.Assign] = RFAssignWrapper()
wrappers[ast.Module] = RFMethodNodeWrapper()


# Finds the rf_ast for the given method name, or generates it if it does not exist
def rf_ast_for_method(class_or_object, method_name):
    return reflective_method_for(class_or_object, method_name).original_ast


def reflective_method_for(class_or_object, method_name):
    rf_key = (class_or_object, method_name)

    if not (is_method_reflective(rf_key)):
        method = getattr(class_or_object, method_name)
        rf_ast = RFAstBuilder().rf_ast_for_method(class_or_object, method, method_name)
        rf_method = ReflectiveMethod(rf_ast, class_or_object)
        rf_methods[rf_key] = rf_method
        return rf_method
    return rf_methods.get(rf_key)


def is_method_reflective(rf_key):
    return rf_key in rf_methods.keys()


def is_node_wrapped(rf_node):
    return rf_node.method_node.reflective_method.is_node_wrapped(rf_node)


def install_metalink(metalink, rf_node):
    metalink.link_to_hook(rf_node.hook)


def link(metalink, rf_node):
    rf_method = rf_node.method_node.reflective_method
    if not rf_method.has_wrappers():
        wrap_node(rf_node.method_node)

    wrap_node(rf_node)
    install_metalink(metalink, rf_node)


def wrap_node(rf_node):
    if is_node_wrapped(rf_node):
        return

    wrapper = wrappers[rf_node.__class__]
    wrapper.method_node = rf_node.method_node
    wrapper_node = wrapper.wrap(rf_node)
    wrapper_node.reflective_method.wrapper_for_node(wrapper_node, rf_node)
    rf_method = rf_node.method_node.reflective_method
    rf_method.recompile()
