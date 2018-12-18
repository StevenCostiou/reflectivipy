import unittest

import Reflectivity
from tests.ReflectivityExample import ReflectivityExample
from core.MetaLink import MetaLink


class MethodWrappingTest(unittest.TestCase):
    def test_wrap_method_node(self):
        example = ReflectivityExample()

        link = MetaLink(example, 'tag_exec_', 'before', [])
        ast = Reflectivity.rf_ast_for_method(ReflectivityExample, 'example_method')

        Reflectivity.link(link, ast)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_method(), 9)
        self.assertEqual(example.tag, 'tag')


if __name__ == '__main__':
    unittest.main()
