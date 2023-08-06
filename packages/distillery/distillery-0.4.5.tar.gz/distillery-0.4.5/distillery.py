# -*- coding: utf-8 -*-

import types
import weakref

#  Stores all lazy attributes for counter creation
_lazies = []
_cache = weakref.WeakValueDictionary()
_scope = []


def lazy(f):
    """Stores the method creation counter and sets it as a classmethod.
    """
    _lazies.append(f)
    f.counter = len(_lazies)
    return classmethod(f)


def get_priority(value):
    if isinstance(value, type) and issubclass(value, Set):
        return SetMeta.classes[value]

    return 0


def iter_bases(cls):
    yield cls

    for base in cls.__bases__:
        if not type(base) is type(cls):
            continue

        for cls in iter_bases(base):
            yield cls


def get_dict(value):
    d = {}
    for base in reversed(list(iter_bases(type(value)))):
        d.update(base.__dict__)

    d.update(value.__dict__)
    return d


def iter_set(fixture):
    members = []

    d = get_dict(fixture)

    for name, value in d.items():
        if name.startswith('_'):
            continue

        members.append((get_priority(value), name))

    if not members:
        return members

    return zip(*sorted(members))[1]


class Distillery(object):
    """Base class for ORM dependent distilleries.
    """
    @classmethod
    def bulk(cls, count, **kwargs):
        """Bluck creates new instances.
        """
        def format(value, i):
            if type(value) in (str, unicode):
                value = value % {'i': str(i)}
            return value

        instances = []
        for i in range(count):

            k = {key: format(kwargs[key], i) for key in kwargs}
            instances.append(cls.create(**k))
        return instances

    @classmethod
    def create(cls, **kwargs):
        """Inits, populates and saves a object instance.
        """
        instance = cls.init(**kwargs)
        instance = cls.save(instance)
        if hasattr(cls, '_after_create'):
            cls._after_create(instance)
        return instance

    @classmethod
    def init(cls, **kwargs):
        """Inits and populate object instance.
        """
        cls._sequence = cls.get_next_sequence()

        def set(instance, attr, value):
            if not attr in dir(instance):
                raise AttributeError("`%s` has no attribute `%s`." \
                    % (instance.__class__.__name__, attr))
            if callable(value):
                value = value(instance)
            setattr(instance, attr, value)

        instance = cls.__model__()

        #  kwargs
        for key in kwargs:
            set(instance, key, kwargs.get(key))

        def get_counter((k, m)):
            return m.counter if hasattr(m, 'counter') else 0

        #  Class members
        #  Sets basic attributes then lazy ones by creation order
        for key, member in sorted([(k, getattr(cls, k)) for k in dir(cls)],
                key=get_counter):
            if not key in Distillery.__dict__ and not key.startswith('_') \
                    and not key in kwargs:
                if callable(member):
                    value = member(instance, cls._sequence)
                else:
                    value = member
                set(instance, key, value)
        return instance

    @classmethod
    def save(cls, instance):
        """Saves given object instance.
        """
        raise NotImplementedError()

    @classmethod
    def get_next_sequence(cls):
        """Returns the next sequence value for lazies.
        """
        if not hasattr(cls, '_sequence'):
            return 0
        return cls._sequence + 1


class SetMeta(type):
    """Adds a `_set_class` property to all fixtures class in a set.
    """

    counter = 0
    classes = weakref.WeakKeyDictionary()

    def __new__(meta, name, bases, dict_):
        meta.counter += 1
        new = type.__new__(meta, name, bases, dict_)
        for key in dict_:
            if not key.startswith('_'):
                member = getattr(new, key)
                if not isinstance(member, types.MethodType):
                    setattr(member, '_set_class', new)
        meta.classes[new] = meta.counter
        return new


class Set(object):
    """Fixtures dataset.
    """
    __metaclass__ = SetMeta

    def __new__(cls, *args, **kwargs):
        """Creates new `cls` instance or return the existing one.
        """

        instance = _cache.get(cls)

        if instance is None:
            instance = super(Set, cls).__new__(cls, *args, **kwargs)
            instance._fixtures = {}
            instance._foreign_sets = {}
            _cache[cls] = instance

        _scope.append(set((instance, )))
        _scope[0].add(instance)

        return instance

    def __init__(self, on_demand=False):
        self._on_demand = on_demand
        try:
            if not on_demand:
                for member in iter_set(self):
                    getattr(self, member)
        finally:
            assert self in _scope.pop()

    def __getattribute__(self, attr):
        if attr.startswith('_'):
            return super(Set, self).__getattribute__(attr)
        if not attr in dir(self):
            raise AttributeError('Invalid fixture `%s`.' % attr)
        if not attr in self._fixtures:
            fixture = super(Set, self).__getattribute__(attr)
            if isinstance(fixture, types.MethodType):
                #  Fixture is a callable
                instance = fixture()
                expected_class = self.__distillery__.__model__
                if not isinstance(instance, expected_class):
                    raise Exception("%s must return a %s instance" % \
                        (fixture, expected_class.__name__))
            elif issubclass(fixture, Set):
                #  Fixture is an embedded set
                instance = self._get_foreign_set_instance(fixture)
            else:
                #  Fixture is a fixture
                kwargs = {}
                for key in dir(fixture):
                    if not key.startswith('_'):
                        kwargs[key] = self._get_member(fixture, key)
                instance = self.__distillery__.create(**kwargs)
            if not issubclass(instance.__class__, Set) and \
                    hasattr(fixture, '_after_create'):
                fixture._after_create(instance)
            self._fixtures[attr] = instance
        return self._fixtures[attr]

    @classmethod
    def _get_instance(cls, on_demand):
        instance = _cache.get(cls)
        if instance is None:
            instance = cls(on_demand)
            _cache[cls] = instance
        return instance

    def _get_foreign_set_instance(self, set_class):
        set_ = set_class._get_instance(self._on_demand)
        self._foreign_sets[set_class.__name__] = set_
        return set_

    def _get_member(self, fixture, key):
        def _get_foreign(member):
            if hasattr(member, '_set_class'):
                set_class = member._set_class
            elif hasattr(member, 'im_class'):
                set_class = member.im_class
            else:
                raise Exception('%s does not appear to be a valid fixture' \
                    % member)
            set_ = self._get_foreign_set_instance(set_class)
            return getattr(set_, member.__name__)

        member = getattr(fixture, key)
        if isinstance(member, list) or isinstance(member, tuple):
            member = [_get_foreign(m) for m in member]
        elif callable(member):
            if hasattr(member, 'im_class') and \
                    not issubclass(member.im_class, Set):
                member = member()
                if hasattr(member, '_set_class'):
                    member = _get_foreign(member)
            else:
                member = _get_foreign(member)
        return member


class DjangoDistillery(Distillery):
    @classmethod
    def save(cls, instance):
        instance.save()
        return instance


class SQLAlchemyDistillery(Distillery):
    @classmethod
    def save(cls, instance):
        cls.__session__.add(instance)
        cls.__session__.flush()
        return instance
