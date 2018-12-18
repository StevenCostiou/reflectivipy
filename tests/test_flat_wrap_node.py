import unittest

import Reflectivity
from tests.ReflectivityExample import ReflectivityExample
from core.MetaLink import MetaLink


class NodeWrapperTest(unittest.TestCase):
    def setUp(self):
        Reflectivity.uninstall_all()

    def tearDown(self):
        Reflectivity.uninstall_all()

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

    def test_after_return(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec_', 'after', [])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_return')
        node = rf_ast.original_ast.body[0].body[0]

        Reflectivity.link(link, node)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_return(), 42)
        self.assertEqual(example.tag, 'tag')

    def test_after_returns_wraps_in_method(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec_', 'after', [])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_multiple_return')
        node = rf_ast.original_ast

        Reflectivity.link(link, node)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_multiple_return(0), 42)
        self.assertEqual(example.tag, 'tag')

        example.tag = None
        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_multiple_return(1), 2)
        self.assertEqual(example.tag, 'tag')
