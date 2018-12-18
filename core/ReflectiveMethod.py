import copy
import ast
from core.RFAstBuilder import RFAstBuilder


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
        self.original_ast = RFAstBuilder().rf_ast_for_method(self.target_entity, self.original_method, self.method_name)
        self.reflective_ast = copy.deepcopy(self.original_ast)
        self.original_ast.reflective_method = self

    def link(self, metalink):
        self.links.add(metalink)

    def compile_rf_method(self, rf_ast, method_name):
        locs = {}
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
        self.links = set()
        self.init_reflective_method()
        self.recompile()
