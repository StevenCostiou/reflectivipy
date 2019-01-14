import ast
from weakref import WeakValueDictionary
from core.ReflectiveMethod import ReflectiveMethod

from wrappers import flat_wrappers

rf_methods = WeakValueDictionary()

metalinks = set()
nodes_with_links = set()


# Finds the rf_ast for the given method name, or generates it if it does not exist
def rf_ast_for_method(class_or_object, method_name):
    return reflective_method_for(class_or_object, method_name).original_ast


def reflective_method_for(class_or_object, method_name):
    rf_key = (class_or_object, method_name)
    try:
        return rf_methods[rf_key]
    except KeyError:
        method = getattr(class_or_object, method_name)
        rf_method = ReflectiveMethod(class_or_object, method, method_name)
        rf_methods[rf_key] = rf_method
        return rf_method


def link(metalink, rf_node):
    metalinks.add(metalink)
    nodes_with_links.add(rf_node)

    metalink.add_node(rf_node)
    # import ast
    # if isinstance(rf_node, ast.Expr):
    #     rf_node = rf_node.value
    rf_node.links.add(metalink)
    rf_node.method_node.reflective_method.invalidate()


def uninstall_all():
    for metalink in metalinks:
        for node in metalink.nodes:
            metalink.remove_node(node)

    for node in nodes_with_links:
        node.links.clear()

    metalinks.clear()
    nodes_with_links.clear()

    for rf_method in rf_methods.values():
        rf_method.restore()
