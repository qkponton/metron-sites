import threading


def singleton(cls):
    """ This is a decorator for classes that make them Singleton object
    (mmeaning, there is always one instanciated object for this class).
    This decorator doesn't work for classes that implements the __new__ method.
    """

    # We make a singleton class (derivate from the original class)
    class SingleClass(cls):
        """ The real singleton. """
        _instance = None
        __module__ = cls.__module__
        __doc__ = cls.__doc__

        def __new__(cls, *args, **kwargs):
            if SingleClass._instance is None:
                SingleClass._instance = super(SingleClass, cls).__new__(cls, *args, **kwargs)
                SingleClass._instance._sealed = False

            return SingleClass._instance

        def __init__(self):
            if not getattr(self, '_sealed', False):
                super().__init__()
                self._sealed = True

    SingleClass.__name__ = cls.__name__
    return SingleClass


class Singleton(type):
    """
    Metaclass to create singleton
    """

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in Singleton._instances:
            with Singleton._lock:
                Singleton._instances.setdefault(cls, super().__call__(*args, **kwargs))
        return Singleton._instances[cls]
