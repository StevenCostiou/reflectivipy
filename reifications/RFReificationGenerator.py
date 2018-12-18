import core.RFAstBuilder
import RFReification


class RFReificationGenerator(object):
    def __init__(self):
        self.builder = core.RFAstBuilder.RFAstBuilder()
        self.reification_counter = 0
        self.arg_list = []

    def generate_reifications(self, rf_node):
        expressions = []

        for link in rf_node.links:
            link.reset_reified_arguments()

            for arg in link.arguments:
                reification = RFReification.reification_for(arg, link).visit_node(rf_node)
                rf_name = self.rf_name_for_arg(arg, str(rf_node.rf_id))
                expressions.append(self.builder.assign_named_value(rf_name, reification))
                self.add_reified_argument_to_link(self.builder.ast_load(rf_name), link)

            if link.option_arg_as_array:
                link.reified_arguments.append(self.builder.ast_load_list(self.arg_list))
                self.arg_list = []

        return expressions

    def add_reified_argument_to_link(self, arg_node, metalink):
        if metalink.option_arg_as_array:
            self.arg_list.append(arg_node)
        else:
            metalink.reified_arguments.append(arg_node)

    def rf_name_for_arg(self, arg, rf_id):
        if isinstance(arg, basestring):
            return arg + '_' + rf_id

        self.reification_counter = self.reification_counter + 1
        return 'value_' + rf_id + '_' + str(self.reification_counter)
