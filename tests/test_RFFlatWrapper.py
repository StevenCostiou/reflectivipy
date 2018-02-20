import unittest
import Reflectivity
import ReflectivityExample
from metalinks.MetaLink import MetaLink
from flat_wrappers.RFFlatWrapper import RFFlatWrapper


class TestRFFlatWrapper(unittest.TestCase):
    def test_sort_links(self):
        before_link = MetaLink(None, None, 'before', [])
        after_link = MetaLink(None, None, 'after', [])
        instead_link = MetaLink(None, None, 'instead', [])
        node = ReflectivityExample.sample_node()

        Reflectivity.link(before_link, node)
        Reflectivity.link(after_link, node)
        Reflectivity.link(instead_link, node)

        wrapper = RFFlatWrapper(node)

        self.assertEqual(len(wrapper.before_links), 0)
        self.assertEqual(len(wrapper.after_links), 0)
        self.assertEqual(len(wrapper.instead_links), 0)

        wrapper.sort_links()

        self.assertEqual(len(wrapper.before_links), 1)
        self.assertIs(wrapper.before_links[0], before_link)

        self.assertEqual(len(wrapper.after_links), 1)
        self.assertIs(wrapper.after_links[0], after_link)

        self.assertEqual(len(wrapper.instead_links), 1)
        self.assertIs(wrapper.instead_links[0], instead_link)
