import reflectivity


def sample_node():
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'example_assign')
    return rf_ast.original_ast.body[0].body[0]


def expr_sample_node():
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'm3')
    return rf_ast.original_ast.body[0].body[0]


def call_sample_node():
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'm3')
    return rf_ast.original_ast.body[0].body[0]


def complex_call_sample_node():
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'example_method')
    return rf_ast.original_ast.body[0].body[1]


def complex_expr_call_sample_node():
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'm4')
    return rf_ast.original_ast.body[0].body[0]


def call_with_complex_receiver_sample_node():
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'm5')
    return rf_ast.original_ast.body[0].body[0]


def value_reification_sample_node():
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'example_value_reification')
    return rf_ast.original_ast.body[0].body[1]


def value_call_reification_sample_node():
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'example_value_call_reification')
    return rf_ast.original_ast.body[0].body[1]


def value_call_call_reification_sample_node():
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'example_value_call_call_reification')
    return rf_ast.original_ast.body[0].body[1]


def value_name_reification_sample_node():
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'example_value_name_reification')
    return rf_ast.original_ast.body[0].body[1].value.args[0]


def method_with_args_sample_node():
    rf_ast = reflectivity.reflective_method_for(ReflectivityExample, 'method_with_args')
    return rf_ast.original_ast


class ReflectivityExample:
    def __init__(self):
        self.tag = None
        self.tagged_reifications = list()

    def tag_exec_(self):
        self.tag = 'tag'

    def tag_exec(self, reifications):
        self.tag = reifications

    def tag_push(self, reification):
        self.tagged_reifications.append(reification)

    def tag_reifications(self, reification_1, reification_2, reification_3, reification_4):
        self.tagged_reifications = list()
        self.tagged_reifications.append(reification_1)
        self.tagged_reifications.append(reification_2)
        self.tagged_reifications.append(reification_3)
        self.tagged_reifications.append(reification_4)

    def example_method(self):
        val = 3 + 4
        val = self.m(self.m2(val))
        return val

    def method_with_args(self, i, j, k):
        val = self.m(j)
        return val + i + k

    def m(self, i):
        return i + 1

    def m2(self, j):
        return j + 1

    def m3(self):
        self.m(0)

    def m4(self):
        self.m(self.m2(42))

    def m5(self):
        self.m6().m(0)

    def m6(self):
        return self

    def example_assign(self):
        a = 1
        return a

    def example_call(self):
        i = 1
        self.m(i)

    def example_assign_call(self):
        i = 1
        a = self.m(i)
        return a

    def example_assign_embedded_calls(self):
        i = 1
        a = self.m(self.m2(i))
        return a

    def example_return(self):
        return 42

    def example_multiple_return(self, i):
        if i == 0:
            return 42
        j = i + 1
        return j

    def example_while(self):
        i = 0
        while i < 10:
            i = i + 1
        return i

    def example_for(self):
        j = 0
        for i in range(10):
            j = j + 1
        return j

    def example_expr_node(self):
        self.m(1)

    def example_value_reification(self):
        i = 1
        i = 2

    def example_value_call_reification(self):
        i = 1
        i = self.m(i)

    def example_value_call_call_reification(self):
        i = self.m(0)
        i = self.m(i)

    def example_value_name_reification(self):
        i = 1
        self.m(i)
