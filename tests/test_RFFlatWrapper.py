import pytest

import reflectivipy
import tests.ReflectivityExample as ReflectivityExample
from reflectivipy import MetaLink
from reflectivipy.wrappers import FlatWrapper


@pytest.fixture(autouse=True)
def setup():
    reflectivipy.uninstall_all()


def test_sort_links():
    before_link = MetaLink(None, None, 'before', [])
    after_link = MetaLink(None, None, 'after', [])
    instead_link = MetaLink(None, None, 'instead', [])
    node = ReflectivityExample.sample_node()

    node.links.append(before_link)
    node.links.append(after_link)
    node.links.append(instead_link)

    wrapper = FlatWrapper(node)

    assert len(wrapper.before_links) == 0
    assert len(wrapper.after_links) == 0
    assert len(wrapper.instead_links) == 0

    wrapper.sort_links()

    assert len(wrapper.before_links) == 1
    assert wrapper.before_links[0] is before_link

    assert len(wrapper.after_links) == 1
    assert wrapper.after_links[0] is after_link

    assert len(wrapper.instead_links) == 1
    assert wrapper.instead_links[0] is instead_link
