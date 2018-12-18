import unittest

import Reflectivity
from tests.ReflectivityExample import ReflectivityExample
from core.MetaLink import MetaLink


class CFlowIFTest(unittest.TestCase):
    def setUp(self):
        Reflectivity.uninstall_all()

    def test_link_before_if(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec_', 'before', [])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_multiple_return')
        node = rf_ast.original_ast.body[0].body[0]

        Reflectivity.link(link, node)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_multiple_return(0), 42)
        self.assertEqual(example.tag, 'tag')

    def test_link_after_if(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec_', 'after', [])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_multiple_return')
        node = rf_ast.original_ast.body[0].body[0]

        Reflectivity.link(link, node)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_multiple_return(1), 2)
        self.assertEqual(example.tag, 'tag')

    def test_link_before_after_if(self):
        example = ReflectivityExample()
        before_link = MetaLink(example, 'tag_push', 'before', [1])
        after_link = MetaLink(example, 'tag_push', 'after', [2])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_multiple_return')
        node = rf_ast.original_ast.body[0].body[0]

        Reflectivity.link(before_link, node)
        Reflectivity.link(after_link, node)

        self.assertEqual(len(example.tagged_reifications), 0)
        self.assertEquals(ReflectivityExample().example_multiple_return(1), 2)
        self.assertEqual(len(example.tagged_reifications), 2)
        self.assertEquals(example.tagged_reifications[0], 1)
        self.assertEquals(example.tagged_reifications[1], 2)

    def test_link_after_if_that_returns_before_link(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec_', 'after', [])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_multiple_return')
        node = rf_ast.original_ast.body[0].body[0]

        Reflectivity.link(link, node)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_multiple_return(0), 42)
        self.assertEqual(example.tag, None)
