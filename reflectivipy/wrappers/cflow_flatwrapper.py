from .flatwrapper import FlatWrapper


class CFlowConditionExtractor(object):
    def __init__(self):
        self.flattened_condition = []
        self.preambles = []
        self.body_supplements = []

    def visit_node(self, rf_node):
        visit_method = "visit_" + rf_node.__class__.__name__
        getattr(self, visit_method)(rf_node)

    def visit_While(self, rf_node):
        test = rf_node.test
        if not test.wrapper.should_wrap(test):
            return
        self.extract_test(test)
        self.preambles = self.flattened_condition
        self.body_supplements = self.flattened_condition

    def visit_For(self, rf_node):
        pass

    def visit_If(self, rf_node):
        test = rf_node.test
        if not test.wrapper.should_wrap(test):
            return
        self.extract_test(test)
        self.preambles = self.flattened_condition

    def extract_test(self, rf_test):
        self.flattened_condition = rf_test.wrapper.flat_wrap()


class CFlowFlatWrapper(FlatWrapper):
    def __init__(self, rf_node):
        super(CFlowFlatWrapper, self).__init__(rf_node)

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
        transformations = []
        for node in self.extract_body():
            if hasattr(node, "can_be_wrapped"):
                body_transformation = node.wrapper.flat_wrap()
                transformations.extend(body_transformation)
        return transformations

    def extract_condition(self):
        extractor = CFlowConditionExtractor()
        extractor.visit_node(self.original_node)
        self.flattened_children.extend(extractor.preambles)
        self.original_node.twin.body.extend(extractor.body_supplements)
