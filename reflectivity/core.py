import copy
import ast
import inspect


class MetaLink(object):
    def __init__(self, metaobject, selector, control="before", arguments=None):
        self.metaobject = metaobject
        self.selector = selector
        self.control = control
        self.nodes = []
        self.arguments = arguments or []
        self.reified_arguments = []
        self.option_arg_as_array = False

    def add_node(self, rf_node):
        self.nodes.append(rf_node)

    def remove_node(self, rf_node):
        self.nodes.remove(rf_node)
        rf_node.links.remove(self)

    def uninstall(self, from_node=None):
        nodes = [from_node] if from_node else list(self.nodes)
        for node in nodes:
            self.remove_node(node)

    def reset_reified_arguments(self):
        self.reified_arguments = []


class ReflectiveMethod(object):
    def __init__(self, class_or_object, method, method_name):
        self.target_entity = class_or_object
        self.method_name = method_name
        self.original_method = method
        self.original_ast = None
        self.reflective_ast = None
        self.links = set()
        self.init_reflective_method()

    def init_reflective_method(self):
        builder = AstBuilder()
        self.original_ast = builder.rf_ast_for_method(
            self.target_entity, self.original_method, self.method_name
        )
        self.reflective_ast = copy.deepcopy(self.original_ast)
        self.original_ast.reflective_method = self

    def link(self, metalink):
        self.links.add(metalink)

    def compile_rf_method(self, rf_ast, method_name):
        locs = {}
        compiled_method = compile(rf_ast, "<ast>", "exec")
        global_vars = {"__rf_original_method__": self.original_method}
        eval(compiled_method, global_vars, locs)
        if not inspect.isclass(self.target_entity):
            method = locs[method_name].__get__(self.target_entity)
        else:
            method = locs[method_name]
        setattr(self.target_entity, method_name, method)

    def recompile(self):
        self.compile_rf_method(self.reflective_ast, self.method_name)

    def invalidate(self):
        self.reflective_ast.body[0].body = self.original_ast.wrapper.flat_wrap()
        ast.fix_missing_locations(self.reflective_ast)
        self.recompile()

    def restore(self):
        self.links = set()
        self.init_reflective_method()
        self.recompile()


class AstBuilder(object):
    def __init__(self):
        self.method_node = None
        self.current_index = 1
        self.flattened_nodes = {}

    def ast_load_list(self, args_list):
        return ast.List(elts=args_list, ctx=ast.Load())

    def assign_named_value(self, name, value):
        value_store = self.ast_store(name)
        return self.ast_assign(value_store, value)

    def ast_assign(self, store_node, value_node):
        return ast.Assign(targets=[store_node], value=value_node)

    def ast_store(self, var_name):
        return ast.Name(id=var_name, ctx=ast.Store())

    def ast_load(self, var_name):
        load = ast.Name(id=var_name, ctx=ast.Load())
        load.temp_name = var_name
        return load

    def ast_expr(self, node):
        return ast.Expr(node)

    @staticmethod
    def get_method_source(method):
        while "__rf_original_method__" in method.__func__.func_globals:
            method = method.__func__.func_globals["__rf_original_method__"]
        lines = inspect.getsourcelines(method)
        src = ""
        for line in lines[0]:
            src += line[4:]
        return src

    @classmethod
    def ast_for_method(cls, method):
        return ast.parse(cls.get_method_source(method))

    def rf_ast_for_method(self, method_class, method, method_name):
        method_node = self.ast_for_method(method)
        method_node.method_name = method_name
        method_node.method_class = method_class
        return self.build_rf_ast(method_node)

    def build_rf_ast(self, node):
        self.method_node = node
        self.method_node.is_method = True
        self.visit_node(self.method_node)
        self.visit_twins(copy.deepcopy(node))
        return node

    def visit_twins(self, copy_node):
        for node in ast.iter_child_nodes(copy_node):
            original_node = self.flattened_nodes[node.rf_id]
            node.method_node = original_node.method_node
            original_node.twin = node
            self.visit_twins(node)

    def visit_node(self, node):
        self.decorate_node(node)

        for child in ast.iter_child_nodes(node):
            child.parent = node
            node.children.append(child)
            self.visit_node(child)

        return node

    def build_rf_node(self, node):
        self.decorate_node(node)
        return self.decorate_node(node)

    def decorate_node(self, node):
        if node != self.method_node:
            node.is_method = False

        node.is_generated = False

        node.rf_id = self.current_index
        self.flattened_nodes[node.rf_id] = node
        self.current_index += 1

        node_class = node.__class__
        node.can_be_wrapped = True
        node.temp_name = "temp_{}_{}".format(node_class.__name__, node.rf_id)

        node.method_node = self.method_node

        node.method_class = self.method_node.method_class
        node.links = set()

        from wrappers import flat_wrappers

        if node_class in flat_wrappers:
            node.wrapper = flat_wrappers[node_class](node)
        else:
            node.wrapper = flat_wrappers["generic"](node)

        node.children = []
        return node
