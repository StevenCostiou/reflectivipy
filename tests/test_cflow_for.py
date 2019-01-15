import pytest

import reflectivity
from tests.ReflectivityExample import ReflectivityExample
from reflectivity import MetaLink


@pytest.fixture(autouse=True)
def setup():
    reflectivity.uninstall_all()


def test_link_before_for():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'before', [])
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'example_for')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivity.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_for() == 10
    assert example.tag == 'tag'


def test_link_after_for():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'after', [])
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'example_for')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivity.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_for() == 10
    assert example.tag == 'tag'


def test_link_before_after_for():
    example = ReflectivityExample()
    before_link = MetaLink(example, 'tag_push', 'before', [1])
    after_link = MetaLink(example, 'tag_push', 'after', [2])
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'example_for')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivity.link(before_link, node)
    reflectivity.link(after_link, node)

    assert len(example.tagged_reifications) == 0
    assert ReflectivityExample().example_for() == 10
    assert len(example.tagged_reifications) == 2
    assert example.tagged_reifications[0] == 1
    assert example.tagged_reifications[1] == 2


def test_link_inside_for():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec_', 'after', [])
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'example_for')
    node = rf_ast.original_ast.body[0].body[1].body[0]

    reflectivity.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_for() == 10
    assert example.tag == 'tag'
