import pytest

import reflectivipy
from tests.ReflectivityExample import ReflectivityExample
from reflectivipy import MetaLink


@pytest.fixture(autouse=True)
def setup():
    reflectivipy.uninstall_all()



def test_link_to_node():
    example = ReflectivityExample()

    link = MetaLink(example, 'tag_exec', 'before', [])
    rf_node = reflectivipy.reflective_ast_for_method(ReflectivityExample, 'example_method')

    reflectivipy.link(link, rf_node)

    assert rf_node.links
    assert rf_node.links.pop() is link

    assert link.nodes
    assert link.nodes.pop() is rf_node


def test_uninstall():
    pass
