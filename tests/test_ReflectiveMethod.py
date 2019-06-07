import pytest

import reflectivipy
from .ReflectivityExample import ReflectivityExample
from reflectivipy import MetaLink


@pytest.fixture(autouse=True)
def setup():
    reflectivipy.uninstall_all()


def test_original_ast_preservation():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'after', ['node'])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_while')
    original_body = rf_ast.original_ast.body[0].body
    node = original_body[1].test.left

    number_of_nodes = len(original_body)
    original_left_id = node.id

    reflectivipy.link(link, node)

    new_body = rf_ast.original_ast.body[0].body
    new_left = new_body[1].test.left
    reflective_ast_body = rf_ast.reflective_ast.body[0].body

    ReflectivityExample().example_while()
    assert example.tag is node
    assert new_body is original_body
    assert len(new_body) == number_of_nodes
    assert original_left_id == new_left.id

    assert reflective_ast_body[1] is not new_body[1]
    assert len(reflective_ast_body) > number_of_nodes


def test_restore_original():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'after', ['node'])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_while')
    original_body = rf_ast.original_ast.body[0].body
    node = original_body[1].test.left

    reflectivipy.link(link, node)

    example.tag = None
    ReflectivityExample().example_while()
    assert example.tag is node

    reflectivipy.uninstall_all()

    example.tag = None
    ReflectivityExample().example_while()
    assert example.tag is None


def test_uninstall_all():
    pass


def test_metalinks_count():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'before', [])
    rf_method = reflectivipy.reflective_method_for(ReflectivityExample, 'example_assign')
    node = rf_method.original_ast.body[0].body[0]

    assert len(reflectivipy.metalinks) == 0

    reflectivipy.link(link, node)

    len(reflectivipy.metalinks) == 1
    assert reflectivipy.metalinks.pop() is link
