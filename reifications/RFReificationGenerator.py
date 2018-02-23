import core.RFAstBuilder
import RFReification


class RFReificationGenerator(object):
    def __init__(self):
        self.builder = core.RFAstBuilder.RFAstBuilder()

    def generate_reifications(self, rf_node):
        expressions = list()

        for link in rf_node.links:
            link.reset_reified_arguments()
            for arg in link.arguments:
                reification = RFReification.reification_for(arg, link).visit_node(rf_node)
                rf_name = self.rf_name_for_arg(arg, str(rf_node.rf_id))
                expressions.append(self.builder.assign_named_value(rf_name, reification))
                self.add_reified_argument_to_link(self.builder.ast_load(rf_name))
        return expressions

    def add_reified_argument_to_link(self, arg_node, metalink):
        metalink.reified_arguments.append(arg_node)

    def rf_name_for_arg(self, arg, rf_id):
        if isinstance(arg, basestring):
            return arg + '_' + rf_id

        return 'value_' + rf_id
