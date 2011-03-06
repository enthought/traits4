import copy

from .event_sys.signals import Signal
from .event_sys.messages import Message
from .event_sys.dispatcher import QueueDispatcher


_queue_dispatcher = QueueDispatcher()


Undefined = object()


class DefaultValueMessage(object):

    def __init__(self, trait_name, obj):
        self.trait_name = trait_name
        self.obj = obj
        self.value = Undefined


class ValidationError(Exception):
    pass


def validation_error(obj, name, val, type_):
    msg = ('The `%s` trait of a `%s` object must be of type `%s` '
           'but a value of type `%s` was received.'
           % (name, obj.__class__.__name__, type_.__name__, 
              type(val).__name__))
    raise ValidationError(msg)


class _Trait:

    def __init__(self, default_value=Undefined, dispatcher=None):
        self._name = ''
        self._default_value = default_value
        self._dispatcher = dispatcher or _queue_dispatcher
        self._validate = Signal()
        self._notify = Signal()
        self._default = Signal()

    def __get__(self, obj, cls):
        name = self._name

        if obj is None:
            raise AttributeError('type object `%s` has no attribute `%s`'
                                 % (cls.__name__, name))
        
        obj_dict = object.__getattribute__(obj, '__dict__')
        if name in obj_dict:
            res = obj_dict[name]
        else:

    def _get_default(self, obj):
        if self._default_value is not Undefined:
            return copy.deepcopy(self._default_value)
        
        msg = DefaultMessage(name, obj)
        self._default.emit(msg, context=obj)
        return self.default
    cdee inline c_validate(self, obj, name, val):
        validation_error(obj, name, val, dict)


cdef class CAny(CTrait):

    cdef inline c_default_value(self, obj, name):
        return None

    cdef inline c_validate(self, obj, name, val):
        return val

