import pytest

import reflectivity
from tests.ReflectivityExample import ReflectivityExample
from core import MetaLink


def test_wrap_method_node():
    example = ReflectivityExample()

    link = MetaLink(example, 'tag_exec_', 'before', [])
    ast = reflectivity.rf_ast_for_method(ReflectivityExample, 'example_method')

    reflectivity.link(link, ast)

    assert example.tag is None
    assert ReflectivityExample().example_method() == 9
    assert example.tag == 'tag'
