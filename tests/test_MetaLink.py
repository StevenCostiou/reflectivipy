import unittest

import Reflectivity
from tests.ReflectivityExample import ReflectivityExample
from core.MetaLink import MetaLink


class MetaLinkTest(unittest.TestCase):
    def test_link_to_node(self):
        example = ReflectivityExample()

        link = MetaLink(example, 'tag_exec', 'before', [])
        rf_node = Reflectivity.rf_ast_for_method(ReflectivityExample, 'example_method')

        Reflectivity.link(link, rf_node)

        self.assertTrue(rf_node.links)
        self.assertIs(rf_node.links.pop(), link)

        self.assertTrue(link.nodes)
        self.assertIs(link.nodes.pop(), rf_node)

    def test_uninstall(self):
        pass


if __name__ == '__main__':
    unittest.main()
