class RFCFlowConditionExtractor(object):
    def __init__(self):
        self.flattened_condition = []
        self.preambles = []
        self.body_supplements = []

    def visit_node(self, rf_node):
        visit_method = 'visit_' + rf_node.__class__.__name__
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
