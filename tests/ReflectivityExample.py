class ReflectivityExample:
    def __init__(self):
        self.tag = None

    def tag_exec(self):
        self.tag = 'tag'

    def tag_exec(self, reifications):
        print(reifications)
        self.tag = 'tag'

    def example_method(self):
        val = 3 + 4
        val = self.m(self.m2(val))
        return val

    def m(self, i):
        return i + 1

    def m2(self, j):
        return j + 1

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
