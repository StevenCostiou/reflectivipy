import copy


class RFAstTwinBuilder(object):
    def build_twins(self, rf_method_node):
        rf_method_node.twin = rf_method_node
        body = rf_method_node.body[0].body
        twin_body = copy.deepcopy(body)

        flattened_original_nodes = self.collect_flattened_original_nodes(body)
        flattened_twin_nodes = self.collect_flattened_original_nodes(twin_body)

        for rf_id in flattened_original_nodes:
            original_node = flattened_original_nodes[rf_id]
            twin_node = flattened_twin_nodes[rf_id]
            self.decorate_twin(original_node, twin_node)
            original_node.twin = twin_node

    def collect_flattened_original_nodes(self, body):
        flattened_nodes = dict()
        for node in body:
            flattened_nodes[node.rf_id] = node
            for child in node.children:
                flattened_nodes[child.rf_id] = child
                self.collect_flattened_original_nodes(child.children)
        return flattened_nodes

    def decorate_twin(self, original_node, twin_node):
        twin_node.method_node = original_node.method_node
        twin_node.wrapping_method_node = original_node.wrapping_method_node
        twin_node.method_class = original_node.method_node.method_class
        twin_node.links = original_node.links
        twin_node.wrapper = original_node.wrapper
