import unittest

import Reflectivity
from tests.ReflectivityExample import ReflectivityExample
from core.MetaLink import MetaLink


class ReflectiveMethodTest(unittest.TestCase):
    def setUp(self):
        Reflectivity.uninstall_all()

    def test_original_ast_preservation(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec', 'after', ['node'])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_while')
        original_body = rf_ast.original_ast.body[0].body
        node = original_body[1].test.left

        number_of_nodes = len(original_body)
        original_left_id = node.id

        Reflectivity.link(link, node)

        new_body = rf_ast.original_ast.body[0].body
        new_left = new_body[1].test.left
        reflective_ast_body = rf_ast.reflective_ast.body[0].body

        ReflectivityExample().example_while()
        self.assertIs(example.tag, node)
        self.assertIs(new_body, original_body)
        self.assertEquals(len(new_body), number_of_nodes)
        self.assertEquals(original_left_id, new_left.id)

        self.assertIsNot(reflective_ast_body[1], new_body[1])
        self.assertGreater(len(reflective_ast_body), number_of_nodes)

    def test_restore_original(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec', 'after', ['node'])
        rf_ast = Reflectivity.reflective_method_for(ReflectivityExample, 'example_while')
        original_body = rf_ast.original_ast.body[0].body
        node = original_body[1].test.left

        Reflectivity.link(link, node)

        example.tag = None
        ReflectivityExample().example_while()
        self.assertIs(example.tag, node)

        Reflectivity.uninstall_all()

        example.tag = None
        ReflectivityExample().example_while()
        self.assertIsNone(example.tag)

    def test_uninstall_all(self):
        pass

    def test_metalinks_count(self):
        example = ReflectivityExample()
        link = MetaLink(example, 'tag_exec_', 'before', [])
        rf_method = Reflectivity.reflective_method_for(ReflectivityExample, 'example_assign')
        node = rf_method.original_ast.body[0].body[0]

        self.assertEqual(len(Reflectivity.metalinks), 0)

        Reflectivity.link(link, node)

        self.assertEqual(len(Reflectivity.metalinks), 1)
        self.assertIs(Reflectivity.metalinks.pop(), link)
