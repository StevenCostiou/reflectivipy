import unittest
import ast
import ReflectivityExample
import Reflectivity
from core.MetaLink import MetaLink


class TestNodeWrapping(unittest.TestCase):
    def setUp(self):
        Reflectivity.uninstall_all()

    def test_wrap_expr(self):
        node = ReflectivityExample.expr_sample_node()

        self.assertEquals(node.__class__, ast.Expr)
        transformation = node.wrapper.flat_wrap()
        self.assertEquals(len(transformation), 1)
        self.assertIs(transformation[0], node)

        link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
        node.links.add(link)

        self.assertEquals(node.__class__, ast.Expr)
        transformation = node.wrapper.flat_wrap()
        self.assertEquals(len(transformation), 1)
        self.assertIs(transformation[0], node)

    def test_wrap_call(self):
        node = ReflectivityExample.call_sample_node().value

        self.assertEquals(node.__class__, ast.Call)
        transformation = node.wrapper.flat_wrap()
        self.assertEquals(len(transformation), 1)
        self.assertIs(transformation[0], node)

        link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
        node.links.add(link)

        self.assertEquals(node.__class__, ast.Call)
        transformation = node.wrapper.flat_wrap()
        self.assertEquals(len(transformation), 4)
        self.assertEquals(transformation[0].__class__, ast.Assign)
        self.assertIs(transformation[0].value, node.args[0])
        self.assertIsNot(transformation[0], node)
        self.assertEquals(len(transformation[3].value.args), 1)
        self.assertEquals(transformation[3].value.args[0].__class__, ast.Name)
        self.assertEquals(transformation[3].value.args[0].id, node.args[0].temp_name)
        self.assertEquals(transformation[3].value.func.value.id, node.func.value.temp_name)

    def test_wrap_call_in_assign(self):
        node = ReflectivityExample.method_with_args_sample_node().body[0].body[0]

        link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
        node.value.links.add(link)

        self.assertEquals(node.__class__, ast.Assign)
        self.assertEquals(node.value.__class__, ast.Call)
        transformation = node.wrapper.flat_wrap()
        self.assertEquals(len(transformation), 5)
        self.assertEquals(transformation[0].__class__, ast.Assign)
        self.assertIs(transformation[0].value, node.value.args[0])
        self.assertEquals(transformation[1].__class__, ast.Assign)
        self.assertEquals(transformation[1].value.id, 'self')
        self.assertIsNot(transformation[0], node)
        self.assertEquals(len(transformation[3].value.args), 1)
        self.assertEquals(transformation[3].value.args[0].__class__, ast.Name)
        self.assertEquals(transformation[3].value.args[0].id, node.value.args[0].temp_name)
        self.assertEquals(transformation[3].value.func.value.id, node.value.func.value.temp_name)

    def test_wrap_complex_expr_call(self):
        node = ReflectivityExample.complex_expr_call_sample_node()

        link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
        node.value.args[0].links.add(link)

        transformation = node.wrapper.flat_wrap()
        self.assertEquals(len(transformation), 6)
        self.assertEquals(transformation[3].__class__, ast.Assign)
        self.assertEquals(transformation[3].value.rf_id, node.value.args[0].rf_id)
        self.assertIsNot(transformation[3], node)

    def test_call_receiver_flattening(self):
        node = ReflectivityExample.call_with_complex_receiver_sample_node()
        link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
        node.value.links.add(link)

        transformation = node.wrapper.flat_wrap()
        self.assertEquals(len(transformation), 4)
        self.assertEquals(transformation[1].value.func.value.id, 'self')
        self.assertEquals(transformation[3].value.func.value.id, transformation[1].targets[0].id)

    def test_call_flattening(self):
        node = ReflectivityExample.call_with_complex_receiver_sample_node()
        link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
        node.value.func.value.links.add(link)

        transformation = node.wrapper.flat_wrap()
        self.assertEquals(len(transformation), 5)
        self.assertEquals(transformation[1].value.id, 'self')
        self.assertEquals(transformation[3].value.func.value.id, transformation[1].targets[0].id)
        self.assertEquals(transformation[4].value.func.value.id, transformation[3].targets[0].id)

    def test_wrap_assign(self):
        node = ReflectivityExample.sample_node()

        self.assertEquals(node.__class__, ast.Assign)
        transformation = node.wrapper.flat_wrap()
        self.assertEquals(len(transformation), 1)
        self.assertIs(transformation[0], node)

        link = MetaLink(ReflectivityExample.ReflectivityExample(), 'tag_exec_', 'before', [])
        node.links.add(link)

        self.assertEquals(node.__class__, ast.Assign)
        transformation = node.wrapper.flat_wrap()
        self.assertEquals(len(transformation), 3)
        self.assertEquals(transformation[0].__class__, ast.Assign)
        self.assertIs(transformation[0].value, node.value)
        self.assertIsNot(transformation[0], node)

    def test_flatten_children(self):
        pass
