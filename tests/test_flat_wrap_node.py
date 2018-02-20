import unittest

import Reflectivity
from metalinks.MetaLink import MetaLink
from tests.ReflectivityExample import ReflectivityExample


class NodeWrapperTest(unittest.TestCase):
    def test_wrap_assign(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec_', 'before', [])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_assign')
        node = rf_ast.original_ast.body[0].body[0]

        Reflectivity.link(link, node)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_assign(), 1)
        self.assertEqual(example.tag, 'tag')

    def test_wrap_assign_with_children(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec_', 'before', [])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_assign_call')
        node = rf_ast.original_ast.body[0].body[1]

        Reflectivity.link(link, node)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_assign_call(), 2)
        self.assertEqual(example.tag, 'tag')
