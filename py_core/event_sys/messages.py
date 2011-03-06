

class Message(object):

    def __init__(self, contents=None):
        self.contents = contents
        self.signal = None # will be set when the signal is emmitted
        
    def initialize(self):
        pass

    def update(self):
        pass

    def finalize(self):
        pass

    def __repr__(self):
        return '%s: %s' % (self.__class__.__name__, str(self.contents))

    def __str__(self):
        return self.__repr__()
