

class Message(object):

    def __init__(self, contents=None):
        self.contents = contents

    def initialize(self):
        pass

    def update(self):
        pass

    def finalize(self):
        pass

    def __repr__(self):
        return 'Message: %s' % str(self.contents)

    def __str__(self):
        return self.__repr__()
