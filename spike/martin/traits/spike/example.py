from martin.traits.spike.simpletype import Simple

from martin.traits.api import HasTraits

    
class Foo(Simple):

    def get_traits(self, inherited=True, **metadata):
        print 'Yowza', inherited, metadata
        return {'a' : 1}
    pass

s = Foo()
s.x = 42

print 's.x', s.x

print s.__dict__

#print 's.x', s.x
#s.x = 42
#print 's.x', s.x
#print 's.y', s.y
