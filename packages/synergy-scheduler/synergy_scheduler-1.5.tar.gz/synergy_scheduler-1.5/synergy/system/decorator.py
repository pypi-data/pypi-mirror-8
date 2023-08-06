__author__ = 'Bohdan Mushkevych'

import sys
import time
import functools
import traceback


def current_process_aware(class_method):
    """
    this decorator is used in ProcessContext to handle case where callers have no notion of the process they run within
    :param class_method: method to wrap
    """

    @functools.wraps(class_method)
    def _class_method(cls, process_name):
        if process_name is None:
            process_name = cls.get_current_process()
        return class_method(cls, process_name)

    return _class_method


def thread_safe(method):
    """ wraps function with lock acquire/release cycle
     decorator requires class instance to have field self.lock of type threading.Lock or threading.RLock """

    @functools.wraps(method)
    def _locker(self, *args, **kwargs):
        try:
            self.lock.acquire()
            return method(self, *args, **kwargs)
        finally:
            try:
                self.lock.release()
            except:
                sys.stderr.write('Exception on releasing lock at method %s' % method.__name__)
                traceback.print_exc(file=sys.stderr)

    return _locker


def with_reconnect(func):
    """
    Handle when AutoReconnect is raised from pymongo. This is the standard error
    raised for everything from "host disconnected" to "couldn't connect to host"
    and more.

    The sleep handles the edge case when the state of a replica set changes, and
    the cursor raises AutoReconnect because the master may have changed. It can
    take some time for the replica set to stop raising this exception, and the
    small sleep and iteration count gives us a couple of seconds before we fail
    completely.
    """
    from pymongo.errors import AutoReconnect

    @functools.wraps(func)
    def _reconnector(*args, **kwargs):
        for _ in xrange(20):
            try:
                return func(*args, **kwargs)
            except AutoReconnect:
                time.sleep(0.250)
        raise

    return _reconnector


def singleton(cls):
    """
    turns class to singleton
    :param cls: class itself
    :return: function that either creates new instance of the class or returns existing one
    """

    # the only way to implement nonlocal closure variables in Python 2.X
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance


def base_model_derived(base_model_class):
    """ wraps setter/getter with a convertor to/from BaseModel and dict """

    def actual_decorator(method):
        @functools.wraps(method)
        def wrapper(self, *args):
            if args:
                # we are in the setter
                if isinstance(args[0], base_model_class):
                    method(self, args[0].document)
                else:
                    method(self, *args)
            else:
                # we are in the getter
                field_value = method(self)
                if isinstance(field_value, dict):
                    return base_model_class(field_value)
                return field_value
        return wrapper
    return actual_decorator
