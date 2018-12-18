import ast
from core.ReflectiveMethod import ReflectiveMethod

from wrappers import flat_wrappers

rf_methods = dict()

metalinks = set()
nodes_with_links = set()


# Finds the rf_ast for the given method name, or generates it if it does not exist
def rf_ast_for_method(class_or_object, method_name):
    return reflective_method_for(class_or_object, method_name).original_ast


def reflective_method_for(class_or_object, method_name):
    rf_key = (class_or_object, method_name)

    if not (rf_key in rf_methods.keys()):
        method = getattr(class_or_object, method_name)
        rf_method = ReflectiveMethod(class_or_object, method, method_name)
        rf_methods[rf_key] = rf_method
        return rf_method
    return rf_methods.get(rf_key)


def link(metalink, rf_node):
    metalinks.add(metalink)
    nodes_with_links.add(rf_node)

    metalink.add_node(rf_node)
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
