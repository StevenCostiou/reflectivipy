import ast
from .cflow_flatwrapper import CFlowFlatWrapper


class MethodFlatWrapper(CFlowFlatWrapper):
    def transform_node(self):
        self.node_transformation.extend(self.transform_body())

    def sort_links(self):
        super(MethodFlatWrapper, self).sort_links()

        body = self.extract_body()
        if not body:
            return

        for rf_node in body:
            self.inject_after_links_in_method_returns(rf_node)

        if self.is_return(self.last_node()):
            self.after_links = []

    def is_return(self, rf_node):
        return rf_node.__class__ is ast.Return

    def extract_body(self):
        return self.original_node.body[0].body

    def last_node(self):
        body = self.extract_body()
        if body:
            return body[-1]
        return None

    def inject_after_links_in_method_returns(self, rf_node):
        if self.is_return(rf_node):
            rf_node.wrapper.additional_after_links.extend(self.after_links)
            return

        for child in rf_node.children:
            self.inject_after_links_in_method_returns(child)
