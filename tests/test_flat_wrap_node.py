import pytest

import reflectivipy
from tests.ReflectivityExample import ReflectivityExample
from reflectivipy import MetaLink


@pytest.fixture(autouse=True)
def setup():
    reflectivipy.uninstall_all()


def test_wrap_assign():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'before', [])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_assign')
    node = rf_ast.original_ast.body[0].body[0]

    reflectivipy.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_assign() == 1
    assert example.tag == 'tag'


def test_wrap_assign_with_children():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'before', [])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_assign_call')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivipy.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_assign_call() == 2
    assert example.tag == 'tag'


def test_after_return():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'after', [])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_return')
    node = rf_ast.original_ast.body[0].body[0]

    reflectivipy.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_return() == 42
    assert example.tag == 'tag'


def test_after_returns_wraps_in_method():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'after', [])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_multiple_return')
    node = rf_ast.original_ast

    reflectivipy.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_multiple_return(0) == 42
    assert example.tag == 'tag'

    example.tag = None
    assert example.tag is None
    assert ReflectivityExample().example_multiple_return(1) == 2
    assert example.tag == 'tag'
