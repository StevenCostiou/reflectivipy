import pytest

import reflectivity
from tests.ReflectivityExample import ReflectivityExample
from reflectivity import MetaLink


@pytest.fixture(autouse=True)
def setup():
    reflectivity.uninstall_all()



def test_link_to_node():
    example = ReflectivityExample()

    link = MetaLink(example, 'tag_exec', 'before', [])
    rf_node = reflectivity.reflective_ast_for_method(ReflectivityExample, 'example_method')

    reflectivity.link(link, rf_node)

    assert rf_node.links
    assert rf_node.links.pop() is link

    assert link.nodes
    assert link.nodes.pop() is rf_node


def test_uninstall():
    pass
