import unittest

import Reflectivity
from tests.ReflectivityExample import ReflectivityExample
from core.MetaLink import MetaLink


class CFlowWhileTest(unittest.TestCase):
    def setUp(self):
        Reflectivity.uninstall_all()

    def test_link_before_while(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec_', 'before', [])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_while')
        node = rf_ast.original_ast.body[0].body[1]

        Reflectivity.link(link, node)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_while(), 10)
        self.assertEqual(example.tag, 'tag')

    def test_link_after_while(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec_', 'after', [])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_while')
        node = rf_ast.original_ast.body[0].body[1]

        Reflectivity.link(link, node)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_while(), 10)
        self.assertEqual(example.tag, 'tag')

    def test_link_before_after_while(self):
        example = ReflectivityExample()
        before_link = MetaLink(example, 'tag_push', 'before', [1])
        after_link = MetaLink(example, 'tag_push', 'after', [2])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_while')
        node = rf_ast.original_ast.body[0].body[1]

        Reflectivity.link(before_link, node)
        Reflectivity.link(after_link, node)

        self.assertEqual(len(example.tagged_reifications), 0)
        self.assertEquals(ReflectivityExample().example_while(), 10)
        self.assertEqual(len(example.tagged_reifications), 2)
        self.assertEquals(example.tagged_reifications[0], 1)
        self.assertEquals(example.tagged_reifications[1], 2)

    def test_link_inside_while(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec_', 'after', [])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_while')
        node = rf_ast.original_ast.body[0].body[1].body[0]

        Reflectivity.link(link, node)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_while(), 10)
        self.assertEqual(example.tag, 'tag')

    def test_link_on_while_after_left_test(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec', 'after', ['node'])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_while')
        node = rf_ast.original_ast.body[0].body[1].test.left

        Reflectivity.link(link, node)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_while(), 10)
        self.assertEqual(example.tag, node)

    def test_multiple_links_within_while(self):
        example = ReflectivityExample()
        link_1 = MetaLink(example, 'tag_push', 'after', [0])
        link_2 = MetaLink(example, 'tag_push', 'after', [1])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_while')
        node_1 = rf_ast.original_ast.body[0].body[1].test.left
        node_2 = rf_ast.original_ast.body[0].body[1].body[0]

        Reflectivity.link(link_1, node_1)
        Reflectivity.link(link_2, node_2)

        self.assertEqual(len(example.tagged_reifications), 0)
        self.assertEquals(ReflectivityExample().example_while(), 10)
        self.assertEqual(len(example.tagged_reifications), 21)

        i = 0
        while i < len(example.tagged_reifications):
            self.assertEqual(example.tagged_reifications[i], i % 2)
            i = i + 1
