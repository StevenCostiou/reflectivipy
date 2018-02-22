from RFFlatWrapper import RFFlatWrapper


class RFCFlowFlatWrapper(RFFlatWrapper, object):
    def extract_body(self):
        return self.original_node.body

    def transform_node(self):
        self.original_node.body = self.transform_body()
        self.node_transformation.append(self.original_node)

    def should_wrap(self, rf_node):
        return True

    def transform_body(self):
        transformations = list()
        for node in self.extract_body():
            body_transformation = node.wrapper.flat_wrap()
            transformations.extend(body_transformation)
        return transformations
