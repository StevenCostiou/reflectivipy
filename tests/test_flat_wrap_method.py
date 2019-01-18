import pytest

import reflectivipy
from tests.ReflectivityExample import ReflectivityExample
from reflectivipy import MetaLink


@pytest.fixture(autouse=True)
def setup():
    reflectivipy.uninstall_all()


def test_wrap_method_node():
    example = ReflectivityExample()

    link = MetaLink(example, 'tag_exec_', 'before', [])
    ast = reflectivipy.reflective_ast_for_method(ReflectivityExample, 'example_method')

    reflectivipy.link(link, ast)

    assert example.tag is None
    assert ReflectivityExample().example_method() == 9
    assert example.tag == 'tag'
