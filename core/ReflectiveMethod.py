import copy
import ast


class ReflectiveMethod(object):
    def __init__(self, original_ast, class_or_object):
        self.target_entity = class_or_object
        self.original_ast = original_ast
        self.original_ast.reflective_method = self
        self.reflective_ast = copy.deepcopy(self.original_ast)
        self.method_name = self.original_ast.body[0].name
        self.links = set()

    def link(self, metalink):
        self.links.add(metalink)

    def compile_rf_method(self, rf_ast, method_name):
        locs = dict()
        compiled_method = compile(rf_ast, "<ast>", 'exec')
        eval(compiled_method, {}, locs)
        setattr(self.target_entity, method_name, locs[method_name])

    def recompile(self):
        self.compile_rf_method(self.reflective_ast, self.method_name)

    def invalidate(self):
        self.reflective_ast.body[0].body = self.original_ast.wrapper.flat_wrap()
        ast.fix_missing_locations(self.reflective_ast)
        self.recompile()

    def restore(self):
        for link in self.links:
            for node in link.nodes:
                node.links.clear()
        self.links = set()
        self.reflective_ast = copy.deepcopy(self.original_ast)
        self.recompile()
