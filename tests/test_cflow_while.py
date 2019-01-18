import pytest

import reflectivipy
from tests.ReflectivityExample import ReflectivityExample
from reflectivipy import MetaLink


@pytest.fixture(autouse=True)
def setup():
    reflectivipy.uninstall_all()


def test_link_before_while():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'before', [])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_while')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivipy.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_while() == 10
    assert example.tag == 'tag'


def test_link_after_while():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'after', [])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_while')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivipy.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_while() == 10
    assert example.tag == 'tag'


def test_link_before_after_while():
    example = ReflectivityExample()
    before_link = MetaLink(example, 'tag_push', 'before', [1])
    after_link = MetaLink(example, 'tag_push', 'after', [2])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_while')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivipy.link(before_link, node)
    reflectivipy.link(after_link, node)

    assert len(example.tagged_reifications) == 0
    assert ReflectivityExample().example_while() == 10
    assert len(example.tagged_reifications) == 2
    assert example.tagged_reifications[0] == 1
    assert example.tagged_reifications[1] == 2


def test_link_inside_while():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'after', [])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_while')
    node = rf_ast.original_ast.body[0].body[1].body[0]

    reflectivipy.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_while() == 10
    assert example.tag == 'tag'


def test_link_on_while_after_left_test():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'after', ['node'])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_while')
    node = rf_ast.original_ast.body[0].body[1].test.left

    reflectivipy.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_while() == 10
    assert example.tag is node


def test_multiple_links_within_while():
    example = ReflectivityExample()
    link_1 = MetaLink(example, 'tag_push', 'after', [0])
    link_2 = MetaLink(example, 'tag_push', 'after', [1])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_while')
    node_1 = rf_ast.original_ast.body[0].body[1].test.left
    node_2 = rf_ast.original_ast.body[0].body[1].body[0]

    reflectivipy.link(link_1, node_1)
    reflectivipy.link(link_2, node_2)

    assert len(example.tagged_reifications) == 0
    assert ReflectivityExample().example_while() == 10
    assert len(example.tagged_reifications) == 21

    for i, reif_value in enumerate(example.tagged_reifications):
        assert reif_value == i % 2
