import ast
from core.ReflectiveMethod import ReflectiveMethod

from wrappers.RFFlatWrapper import RFFlatWrapper
from wrappers.RFAssignFlatWrapper import RFAssignFlatWrapper
from wrappers.RFReturnFlatWrapper import RFReturnFlatWrapper
from wrappers.RFMethodFlatWrapper import RFMethodFlatWrapper
from wrappers.RFCFlowFlatWrapper import RFCFlowFlatWrapper
from wrappers.RFCompareFlatWrapper import RFCompareFlatWrapper
from wrappers.RFLiteralFlatWrapper import RFLiteralFlatWrapper
from wrappers.RFExprFlatWrapper import RFExprFlatWrapper
from wrappers.RFCallFlatWrapper import RFCallFlatWrapper
from wrappers import flat_wrappers

flat_wrappers[ast.Assign] = RFAssignFlatWrapper
flat_wrappers[ast.Return] = RFReturnFlatWrapper
flat_wrappers[ast.Module] = RFMethodFlatWrapper
flat_wrappers[ast.If] = RFCFlowFlatWrapper
flat_wrappers[ast.While] = RFCFlowFlatWrapper
flat_wrappers[ast.For] = RFCFlowFlatWrapper
flat_wrappers[ast.Compare] = RFCompareFlatWrapper
flat_wrappers[ast.Num] = RFLiteralFlatWrapper
flat_wrappers[ast.Str] = RFLiteralFlatWrapper
flat_wrappers[ast.Name] = RFLiteralFlatWrapper
flat_wrappers[ast.Expr] = RFExprFlatWrapper
flat_wrappers[ast.Call] = RFCallFlatWrapper
flat_wrappers['generic'] = RFFlatWrapper

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

