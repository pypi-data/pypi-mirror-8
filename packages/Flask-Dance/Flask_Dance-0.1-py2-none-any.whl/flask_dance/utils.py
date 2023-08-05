from __future__ import unicode_literals

class proxy_property(object):
    def __init__(self, name, pass_self=True, doc=None):
        self.name = name
        self.pass_self = pass_self
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        getter_name = "get_{name}".format(name=self.name)
        getter_func = getattr(obj, getter_name, None)
        if getter_func is None:
            raise AttributeError("Undefined function {}".format(getter_name))
        args = []
        if self.pass_self:
            args.insert(0, obj)
        return getter_func(*args)

    def __set__(self, obj, value):
        setter_name = "set_{name}".format(name=self.name)
        setter_func = getattr(obj, setter_name, None)
        if setter_func is None:
            raise AttributeError("Undefined function {}".format(setter_name))
        args = [value]
        if self.pass_self:
            args.insert(0, obj)
        return setter_func(*args)

    def __delete__(self, obj):
        deleter_name = "delete_{name}".format(name=self.name)
        deleter_func = getattr(obj, deleter_name, None)
        if deleter_func is None:
            raise AttributeError("Undefined function {}".format(deleter_name))
        args = []
        if self.pass_self:
            args.insert(0, obj)
        return deleter_func(*args)