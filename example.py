
from traits import *


class Foo(HasTraits):

    a = Int

    @on_trait_change('a')
    def printer(self, name, old, new):
        print 'static printer'


def printer(*args):
    print 'dynamic printer'

f = Foo()
f2 = Foo()

print 'default f.a: ', f.a
print 'default f2.a: ', f2.a

f.a = 12
f2.a = 42

f.on_trait_change('a', printer)

f.a = 56
f2.a = 19

f.a = 'k' # will raise ValidationError
