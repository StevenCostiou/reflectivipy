import ast
from RFCFlowFlatWrapper import RFCFlowFlatWrapper


class RFMethodFlatWrapper(RFCFlowFlatWrapper, object):
    def transform_node(self):
        self.node_transformation.extend(self.transform_body())

    def sort_links(self):
        super(RFMethodFlatWrapper, self).sort_links()

        body = self.extract_body()
        if not body:
            return

        for rf_node in body:
            self.inject_after_links_in_method_returns(rf_node)

        if self.is_return(self.last_node()):
            self.after_links = list()

    def is_return(self, rf_node):
        return rf_node.__class__ == ast.Return

    def extract_body(self):
        return self.original_node.body[0].body

    def last_node(self):
        body = self.extract_body()
        if body:
            return body[len(body) - 1]
        return None

    def inject_after_links_in_method_returns(self, rf_node):
        if self.is_return(rf_node):
            rf_node.wrapper.additional_after_links.extend(self.after_links)
            return

        for child in rf_node.children:
            self.inject_after_links_in_method_returns(child)
