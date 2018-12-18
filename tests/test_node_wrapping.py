import pytest
import ast
import ReflectivityExample
import Reflectivity
from core.MetaLink import MetaLink


@pytest.fixture(autouse=True)
def setup():
    Reflectivity.uninstall_all()


def test_wrap_expr():
    node = ReflectivityExample.expr_sample_node()

    assert type(node) is ast.Expr

    transformation = node.wrapper.flat_wrap()
    assert len(transformation) == 1
    assert transformation[0] is node

    link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
    node.links.add(link)

    assert type(node) is ast.Expr
    transformation = node.wrapper.flat_wrap()
    assert len(transformation) == 1
    assert transformation[0] is node


def test_wrap_call():
    node = ReflectivityExample.call_sample_node().value

    assert type(node) is ast.Call

    transformation = node.wrapper.flat_wrap()
    assert len(transformation) == 1
    assert transformation[0] is node

    link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
    node.links.add(link)

    assert type(node) is ast.Call

    transformation = node.wrapper.flat_wrap()
    assert len(transformation) == 4
    assert type(transformation[0]) is ast.Assign
    assert transformation[0].value is node.args[0]
    assert transformation[0] is not node

    assert len(transformation[3].value.args) == 1
    assert type(transformation[3].value.args[0]) is ast.Name
    assert transformation[3].value.args[0].id is node.args[0].temp_name
    assert transformation[3].value.func.value.id is node.func.value.temp_name


def test_wrap_call_in_assign():
    node = ReflectivityExample.method_with_args_sample_node().body[0].body[0]

    link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
    node.value.links.add(link)

    assert type(node) is ast.Assign
    assert type(node.value) is ast.Call

    transformation = node.wrapper.flat_wrap()
    assert len(transformation) == 5
    assert type(transformation[0]) == ast.Assign
    assert transformation[0].value is node.value.args[0]
    assert type(transformation[1]) is ast.Assign
    assert transformation[1].value.id == 'self'
    assert transformation[0] is not node
    assert len(transformation[3].value.args) == 1
    assert type(transformation[3].value.args[0]) is ast.Name
    assert transformation[3].value.args[0].id is node.value.args[0].temp_name
    assert transformation[3].value.func.value.id is node.value.func.value.temp_name


def test_wrap_complex_expr_call():
    node = ReflectivityExample.complex_expr_call_sample_node()

    link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
    node.value.args[0].links.add(link)

    transformation = node.wrapper.flat_wrap()
    assert len(transformation) == 6
    assert type(transformation[3]) is ast.Assign
    assert transformation[3].value.rf_id is node.value.args[0].rf_id
    assert transformation[3] is not node


def test_call_receiver_flattening():
    node = ReflectivityExample.call_with_complex_receiver_sample_node()
    link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
    node.value.links.add(link)

    transformation = node.wrapper.flat_wrap()
    assert len(transformation) == 4
    assert transformation[1].value.func.value.id == 'self'
    assert transformation[3].value.func.value.id == transformation[1].targets[0].id


def test_call_flattening():
    node = ReflectivityExample.call_with_complex_receiver_sample_node()
    link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
    node.value.func.value.links.add(link)

    transformation = node.wrapper.flat_wrap()
    assert len(transformation) == 5
    assert transformation[1].value.id == 'self'
    assert transformation[3].value.func.value.id == transformation[1].targets[0].id
    assert transformation[4].value.func.value.id == transformation[3].targets[0].id


def test_wrap_assign():
    node = ReflectivityExample.sample_node()

    assert type(node) is ast.Assign

    transformation = node.wrapper.flat_wrap()
    assert len(transformation) == 1
    assert transformation[0] is node

    link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
    node.links.add(link)

    assert type(node) is ast.Assign

    transformation = node.wrapper.flat_wrap()
    assert len(transformation) == 3
    assert type(transformation[0]) is ast.Assign
    assert transformation[0].value is node.value
    assert transformation[0] is not node


def test_flatten_children():
    pass
