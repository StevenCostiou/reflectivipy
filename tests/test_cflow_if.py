import pytest

import reflectivipy
from reflectivipy import MetaLink
from tests.ReflectivityExample import ReflectivityExample


@pytest.fixture(autouse=True)
def setup():
    reflectivipy.uninstall_all()


def test_link_before_if():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'before', [])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_multiple_return')
    node = rf_ast.original_ast.body[0].body[0]

    reflectivipy.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_multiple_return(0) == 42
    assert example.tag == 'tag'


def test_link_after_if():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'after', [])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_multiple_return')
    node = rf_ast.original_ast.body[0].body[0]

    reflectivipy.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_multiple_return(1) == 2
    assert example.tag == 'tag'


def test_link_before_after_if():
    example = ReflectivityExample()
    before_link = MetaLink(example, 'tag_push', 'before', [1])
    after_link = MetaLink(example, 'tag_push', 'after', [2])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_multiple_return')
    node = rf_ast.original_ast.body[0].body[0]

    reflectivipy.link(before_link, node)
    reflectivipy.link(after_link, node)

    assert len(example.tagged_reifications) == 0
    assert ReflectivityExample().example_multiple_return(1) == 2
    assert len(example.tagged_reifications) == 2
    assert example.tagged_reifications[0] == 1
    assert example.tagged_reifications[1] == 2


def test_link_after_if_that_returns_before_link():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'after', [])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_multiple_return')
    node = rf_ast.original_ast.body[0].body[0]

    reflectivipy.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_multiple_return(0) == 42
    assert example.tag is None
