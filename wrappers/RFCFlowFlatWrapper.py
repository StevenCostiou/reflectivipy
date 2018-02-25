import copy
from RFFlatWrapper import RFFlatWrapper
from RFCFlowConditionExtractor import RFCFlowConditionExtractor


class RFCFlowFlatWrapper(RFFlatWrapper, object):
    def __init__(self, rf_node):
        super(RFCFlowFlatWrapper, self).__init__(rf_node)
        # self.copy_node = self.original_node.twin
        # self.copy_node = copy.deepcopy(rf_node)
        # self.original_node.twin = self.copy_node

    def extract_body(self):
        return self.original_node.body

    def transform_node(self):
        # TODO : node transformation here
        self.original_node.twin.body = self.transform_body()
        self.extract_condition()
        self.node_transformation.append(self.original_node.twin)

    def should_wrap(self, rf_node):
        return True

    def transform_body(self):
        transformations = list()
        for node in self.extract_body():
            if hasattr(node, 'can_be_wrapped'):
                body_transformation = node.wrapper.flat_wrap()
                transformations.extend(body_transformation)
        return transformations

    def extract_condition(self):
        extractor = RFCFlowConditionExtractor()
        extractor.visit_node(self.original_node)
        self.flattened_children.extend(extractor.preambles)
        self.original_node.twin.body.extend(extractor.body_supplements)
