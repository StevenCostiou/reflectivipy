import pytest

import reflectivipy
from tests.ReflectivityExample import ReflectivityExample
from reflectivipy import MetaLink
from functools import wraps


@pytest.fixture(autouse=True)
def setup():
    reflectivipy.uninstall_all()


def test_globals_metalink_registry():
    example = ReflectivityExample()

    link = MetaLink(example, 'tag_exec', 'before', [])
    rf_node = reflectivipy.reflective_ast_for_method(ReflectivityExample, 'example_method')

    reflectivipy.link(link, rf_node)

    rf_method = reflectivipy.reflective_method_for(ReflectivityExample, 'example_method')
    method_globals = ReflectivityExample.example_method.func_globals

    assert method_globals["__rf_method__"] is rf_method
    assert method_globals["__rf_method__"].lookup_link(hash(link)) is link


def test_link_to_node():
    example = ReflectivityExample()

    link = MetaLink(example, 'tag_exec', 'before', [])
    rf_node = reflectivipy.reflective_ast_for_method(ReflectivityExample, 'example_method')

    reflectivipy.link(link, rf_node)

    assert rf_node.links
    assert rf_node.links.pop() is link

    assert link.nodes
    assert link.nodes.pop() is rf_node


def test_uninstall():
    pass


decorator_counter = 0


def decorate_with(increment):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            global decorator_counter
            decorator_counter += increment
            print(decorator_counter)
            return f(*args, **kwargs)
        return wrapper
    return decorator


def test_metalinks_with_wrappers():

    class MetaBehavior(object):
        def __init__(self):
            self.called = 0

        def meta(self):
            self.called += 1


    class MyClass(object):
        @decorate_with(1)
        @decorate_with(2)
        @decorate_with(3)
        def da_call(self):
            return 1234

    m = MyClass()
    metabehavior = MetaBehavior()

    link = reflectivipy.MetaLink(metabehavior, selector='meta', control='before')
    rf_ast = reflectivipy.reflective_ast_for_method(m, 'da_call')

    node = rf_ast.body[0].body[0]

    reflectivipy.link(link, node)

    result = m.da_call()

    assert result == 1234
    assert decorator_counter == 6
    assert metabehavior.called == 1
