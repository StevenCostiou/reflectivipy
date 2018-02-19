from compiler.ast_tools import *


class RFNodeWrapper:
    def __init__(self):
        self.method_node = None

    def wrap(self, rf_node):
        wrapper_node = self.create_wrapper_node_for(rf_node)
        self.replace_node_by_wrapper(rf_node, wrapper_node)
        self.compile_wrapper_node(wrapper_node)
        return wrapper_node

    # What about the params?? TODO
    # We must pass the local context variables to the wrapper
    def create_wrapper_node_for(self, rf_node):
        rf_method = rf_node.method_node.reflective_method
        wrapper_node = self.base_wrapper_node_from(rf_method)
        wrapper_node.reflective_method = rf_node.method_node.reflective_method

        reifications = self.reifications_node_for(rf_node)

        new_body = list()
        new_body.append(rf_node.hook.gen_before_call_node(reifications))
        new_body.append(self.basic_wrap(rf_node))
        new_body.append(rf_node.hook.gen_after_call_node(reifications))
        new_body.append(ast.Return(gen_var_read_node('return_val')))

        wrapper_node.body[0].body = new_body
        ast.fix_missing_locations(wrapper_node)

        return wrapper_node

    def base_wrapper_node_from(self, rf_method):
        return rf_method.new_wrapper_node()

    def reifications_node_for(self, rf_node):
        keys = list()
        values = list()
        keys.append(ast.Str('entity'))
        values.append(gen_var_read_node('self'))

        keys.append(ast.Str('class'))
        values.append(ast.Const(rf_node.method_node.method_class))

        return ast.Dict(keys=keys, values=values)

    def basic_wrap(self, rf_node):
        return

    def return_val_name(self):
        return 'return_val'

    def store_node_for_return(self):
        return gen_ast_store(self.return_val_name())

    def compile_wrapper_node(self, wrapper_node):
        method_name = wrapper_node.body[0].name
        wrapper_node.reflective_method.compile_rf_method(wrapper_node, method_name)

    # Replaces a node by a wrapper node in the method or function
    # where the node is defined;
    def replace_node_by_wrapper(self, rf_node, wrapper_node):
        parent_method_node = rf_node.method_node.reflective_method.wrapped_ast
        new_body = []

        for node in parent_method_node.body[0].body:
            if node == rf_node:
                new_body.append(rf_node)
            else:
                new_body.append(node)

        parent_method_node.body[0].body = new_body
        ast.fix_missing_locations(parent_method_node)

    def inject_wrapper_node(self, rf_node, wrapper_node, body):
        return

    def wrapper_call_node(self, wrapper_node):
        method_name = wrapper_node.body[0].name
        method_args = []
        return self.generate_call_to_wrapped(method_name, method_args)

    def set_wrapping_method_node_for_children(self, rf_node, wrapping_method_node):
        pass

    def generate_call_to_wrapped(self, method_name, args):
        value = ast.Name(id="self", ctx=ast.Load())
        attr = ast.Attribute(value=value, attr=method_name, ctx=ast.Load())
        return ast.Call(func=attr, args=args, keywords=[])
