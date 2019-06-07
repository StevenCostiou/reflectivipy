import pytest

import reflectivipy
from reflectivipy import MetaLink

from .ReflectivityExample import ReflectivityExample
from .ReflectivityExample import call_with_complex_receiver_sample_node
from .ReflectivityExample import value_reification_sample_node
from .ReflectivityExample import value_call_reification_sample_node
from .ReflectivityExample import value_call_call_reification_sample_node
from .ReflectivityExample import value_name_reification_sample_node
from .ReflectivityExample import method_with_args_sample_node


@pytest.fixture(autouse=True)
def setup():
    reflectivipy.uninstall_all()


def test_class_reification():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['class'])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_assign_call')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivipy.link(link, node)

    assert example.tag is None

    ReflectivityExample().example_assign_call() == 2
    assert example.tag is ReflectivityExample


def test_literal_value_reification():
    example = ReflectivityExample()
    an_object = ReflectivityExample()
    link = MetaLink(example, 'tag_reifications', 'before', [an_object, 42, "hello", None])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_assign_call')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivipy.link(link, node)

    assert len(example.tagged_reifications) is 0
    assert ReflectivityExample().example_assign_call() == 2
    assert example.tagged_reifications[0] is an_object
    assert example.tagged_reifications[1] is 42
    assert example.tagged_reifications[2] is "hello"
    assert example.tagged_reifications[3]is None


def test_object_reification():
    example = ReflectivityExample()
    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['object'])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_assign_call')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivipy.link(link, node)

    assert example.tag is None
    assert working_example.example_assign_call() == 2
    assert example.tag is working_example


def test_node_reification():
    example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['node'])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_assign_call')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivipy.link(link, node)

    assert example.tag is None
    assert ReflectivityExample().example_assign_call() == 2
    assert example.tag is node


def test_method_reification():
    example = ReflectivityExample()
    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['method'])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_assign_call')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivipy.link(link, node)

    assert example.tag is None
    assert working_example.example_assign_call() == 2
    assert example.tag.__name__, getattr(ReflectivityExample, 'example_assign_call').__name__


def test_multiple_reifications():
    example = ReflectivityExample()
    an_object = ReflectivityExample()
    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_reifications', 'after', ['class', 'object', 'node', an_object])
    rf_ast = reflectivipy.reflective_method_for(ReflectivityExample, 'example_assign_call')
    node = rf_ast.original_ast.body[0].body[1]

    reflectivipy.link(link, node)

    assert len(example.tagged_reifications) == 0
    assert working_example.example_assign_call() == 2
    assert len(example.tagged_reifications) == 4
    assert example.tagged_reifications[0] is ReflectivityExample
    assert example.tagged_reifications[1] is working_example
    assert example.tagged_reifications[2] is node
    assert example.tagged_reifications[3] is an_object


def test_receiver_reification():
    example = ReflectivityExample()
    node = call_with_complex_receiver_sample_node().value.func.value

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['receiver'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.m5()
    assert example.tag is working_example


def test_call_receiver_reification():
    example = ReflectivityExample()
    node = call_with_complex_receiver_sample_node().value

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['receiver'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.m5()
    assert example.tag is working_example


def test_selector_reification():
    example = ReflectivityExample()
    node = call_with_complex_receiver_sample_node().value

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['selector'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.m5()
    assert example.tag == 'm'


def test_sender_reification():
    example = ReflectivityExample()
    node = call_with_complex_receiver_sample_node().value

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['sender'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.m5()
    assert example.tag == 'm5'


def test_assignment_values_reification():
    example = ReflectivityExample()
    node = call_with_complex_receiver_sample_node().value.func.value

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['receiver'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.m5()
    assert example.tag is working_example


def test_read_values_reification():
    example = ReflectivityExample()
    node = call_with_complex_receiver_sample_node().value.func.value

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['receiver'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.m5()
    assert example.tag is working_example


def test_assignment_name_reification():
    example = ReflectivityExample()
    node = value_reification_sample_node()

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['name'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.example_value_reification()
    assert example.tag == 'i'


def test_read_name_reification():
    example = ReflectivityExample()
    node = value_reification_sample_node()

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['name'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.example_value_reification()
    assert example.tag == 'i'


def test_arguments_reification():
    example = ReflectivityExample()
    node = call_with_complex_receiver_sample_node().value.func.value

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['receiver'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.m5()
    assert example.tag is working_example


def test_old_value_reification_assign():
    example = ReflectivityExample()
    node = value_reification_sample_node()

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['old_value'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.example_value_reification()
    assert example.tag == 1


def test_new_value_reification_assign():
    example = ReflectivityExample()
    node = value_reification_sample_node()

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['new_value'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.example_value_reification()
    assert example.tag == 2


def test_value_reification_assign():
    example = ReflectivityExample()
    node = value_reification_sample_node()

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['value'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.example_value_reification()
    assert example.tag == 1


def test_value_reification_name():
    example = ReflectivityExample()
    node = value_name_reification_sample_node()

    working_example = ReflectivityExample()
    link_1 = MetaLink(example, 'tag_push', 'before', ['value'])
    link_2 = MetaLink(example, 'tag_push', 'before', ['old_value'])
    link_3 = MetaLink(example, 'tag_push', 'before', ['new_value'])

    reflectivipy.link(link_1, node)
    reflectivipy.link(link_2, node)
    reflectivipy.link(link_3, node)

    assert example.tag is None

    working_example.example_value_name_reification()
    assert len(example.tagged_reifications) == 3
    assert example.tagged_reifications[0] == 1
    assert example.tagged_reifications[1] == 1
    assert example.tagged_reifications[2] == 1


def test_old_value_with_call_reification():
    example = ReflectivityExample()
    node = value_call_reification_sample_node()

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['old_value'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.example_value_call_reification()
    assert example.tag == 1


def test_new_value_with_call_reification():
    example = ReflectivityExample()
    node = value_call_reification_sample_node()

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['new_value'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.example_value_call_reification()
    assert example.tag == 2


def test_value_with_call_reification():
    example = ReflectivityExample()
    node = value_call_reification_sample_node()

    working_example = ReflectivityExample()
    link = MetaLink(example, 'tag_exec', 'before', ['value'])

    reflectivipy.link(link, node)
    assert example.tag is None

    working_example.example_value_call_reification()
    assert example.tag == 1


def test_value_with_call_call_reification():
    example = ReflectivityExample()
    node = value_call_call_reification_sample_node()

    working_example = ReflectivityExample()

    link_1 = MetaLink(example, 'tag_push', 'before', ['value'])
    link_2 = MetaLink(example, 'tag_push', 'before', ['old_value'])
    link_3 = MetaLink(example, 'tag_push', 'before', ['new_value'])

    reflectivipy.link(link_1, node)
    reflectivipy.link(link_2, node)
    reflectivipy.link(link_3, node)

    assert example.tag is None

    working_example.example_value_call_call_reification()
    assert len(example.tagged_reifications) == 3
    assert example.tagged_reifications[0] == 1
    assert example.tagged_reifications[1] == 1
    assert example.tagged_reifications[2] == 2


def test_named_argument_reification_method():
    pass


def test_argument_as_array_reification_method():
    example = ReflectivityExample()
    method_node = method_with_args_sample_node()

    link = MetaLink(example, 'tag_exec', 'before', ['arguments'])
    reflectivipy.link(link, method_node)

    assert example.tag is None

    res = ReflectivityExample().method_with_args(1, 2, 3)
    assert res == 7

    tab = example.tag
    assert len(tab) == 3
    assert tab[0] == 1
    assert tab[1] == 2
    assert tab[2] == 3


def test_named_argument_reification_call():
    pass


def test_argument_as_array_reification_call():
    example = ReflectivityExample()
    call_node = method_with_args_sample_node().body[0].body[0].value

    link = MetaLink(example, 'tag_exec', 'before', ['arguments'])
    reflectivipy.link(link, call_node)

    assert example.tag is None

    res = ReflectivityExample().method_with_args(1, 2, 3)
    assert res == 7

    tab = example.tag
    assert len(tab) == 1
    assert tab[0] == 2


def test_option_args_as_array_reification_call():
    example = ReflectivityExample()
    call_node = method_with_args_sample_node().body[0].body[0].value

    link = MetaLink(example, 'tag_exec', 'before', ['arguments', 'link', 'class'])
    link.option_arg_as_array = True
    reflectivipy.link(link, call_node)

    assert example.tag is None

    res = ReflectivityExample().method_with_args(1, 2, 3)
    assert res == 7

    tab = example.tag
    assert len(tab) == 3
