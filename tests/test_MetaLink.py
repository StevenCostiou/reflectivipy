import unittest

import Reflectivity
import metalinks.MetaLink as MetaLink

from tests.ReflectivityExample import ReflectivityExample


class MetaLinkTest(unittest.TestCase):
    def test_wrap_method_node(self):
        example = ReflectivityExample()

        link = MetaLink.before(example, 'tag_exec')
        ast = Reflectivity.rf_ast_for_method(ReflectivityExample, 'example_method')

        Reflectivity.old_link(link, ast)

        self.assertEqual(example.tag, None)
        self.assertEquals(ReflectivityExample().example_method(), 9)
        self.assertEqual(example.tag, 'tag')


if __name__ == '__main__':
    unittest.main()
