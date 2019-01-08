import pytest

import Reflectivity
from tests.ReflectivityExample import ReflectivityExample
from core import MetaLink


def test_wrap_method_node():
    example = ReflectivityExample()

    link = MetaLink(example, 'tag_exec_', 'before', [])
    ast = Reflectivity.rf_ast_for_method(ReflectivityExample, 'example_method')

    Reflectivity.link(link, ast)

    assert example.tag is None
    assert ReflectivityExample().example_method() == 9
    assert example.tag == 'tag'
