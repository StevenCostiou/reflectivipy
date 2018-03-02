from RFFlatWrapper import RFFlatWrapper


class RFExprFlatWrapper(RFFlatWrapper, object):
    def flat_wrap(self):
        self.reset_wrapping()
        if self.should_wrap_children(self.original_node):
            self.body.extend(self.original_node.value.wrapper.flat_wrap())
        else:
            self.body.append(self.original_node)
        return self.body
