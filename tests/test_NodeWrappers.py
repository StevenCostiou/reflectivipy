import unittest

import Reflectivity
import metalinks.MetaLink as MetaLink
from tests.ReflectivityExample import ReflectivityExample


class NodeWrapperTest(unittest.TestCase):
    def test_wrap_single_node(self):
        example = ReflectivityExample()
        link = MetaLink.before(example, 'tag_exec')
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_assign')
        node = rf_ast.original_ast.body[0].body[0]

        Reflectivity.old_link(link, node)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_assign(), 1)
        self.assertEqual(example.tag, 'tag')
