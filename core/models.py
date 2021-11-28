""" Django-like model managemnet """

from sqlalchemy import Sequence
from core import settings
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Boolean, Float
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute

Base = declarative_base()
Session = sessionmaker(bind=settings.ENGINE)


def serialize(instance):
    result = {}
    for attribute in dir(instance.__class__):
        a = getattr(instance.__class__, attribute)
        if isinstance(a, InstrumentedAttribute):
            value = getattr(instance, a.key)
            #print(a.key, type(value))
            if not isinstance(value, (str, int, list, type(None))):
                if a.key != 'users':
                    value = serialize(value)
            if a.key != 'users' and a.key != 'owner': #qfix
                result[a.key] = value

    return result


# https://izziswift.com/how-to-create-a-read-only-class-property-in-python/
class managerclassproperty(object):
    """ Setting manager as readonly property """
    def __init__(self, getter):
        self.getter = getter
    def __get__(self, instance, cls=None):
        """ Property getter. Deny access if model class is an instance """
        if instance is not None:
            raise AttributeError("Manager isn't accessible via %s instances" % cls.__name__)
        else:
            return self.getter(cls)

class Manager():

    def __init__(self, model):
        self.model = model
        self.session = Session()

    def get_queryset(self):
        return self.session.query(self.model).all()

    def all(self):
        return self.get_queryset()

    def count(self):
        return self.session.query(self.model).count()

    def create(self, *args, **kwargs):
        obj = self.model(*args, **kwargs)
        self.session.add(obj)
        self.session.commit()

    def delete(self, instance):
        self.session.delete(instance)
        self.session.commit()

    def distinct(self):
        return self.session.query(self.model).distinct()

    def filter(self, **kwargs):
        return self.session.query(self.model).filter_by(**kwargs)

    def get(self, **kwargs):
        return self.session.query(self.model).one(**kwargs)

    def first(self):
        return self.session.query(self.model).first()

    def last(self):
        return self.session.query(self.model).last()

    def order_by(self, *args, **kwargs):
        return self.session.query(self.model).order_by(*args, **kwargs)

    def update(self, instance, **kwargs):
        pass
        # self.session.query(self.model).filter_by(**kwargs).one()
        # return self.session.query(self.model).update(*args, **kwargs)
    
    def raw(self):
        pass

    @property
    def original(self):
        return self.session.query(self.model)

    def values_list(self):
        v_list = []
        qs = self.session.query(self.model).all()

        for query in qs:
            v_list.append(serialize(query))
        
        return v_list

class BaseModelMixin:

    @declared_attr
    def __tablename__(cls):
        _meta = getattr(cls, 'Meta', None)

        if _meta is not None:
            if hasattr(_meta, '__tablename__'):
                return  getattr(_meta, '__tablename__', None)

        return cls.__name__.lower() + 's' # type:ignore

    @managerclassproperty
    def objects(cls):
        return Manager(cls)

    def __get_pk__(self):
        """ Get primary key value """
        if len(inspect(self.__class__).primary_key) > 1:
            raise AttributeError('More than one primery_key')
        return getattr(self, inspect(self.__class__).primary_key[0].name)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self)

    def __str__(self):
        return '%s object (%s)' % (self.__class__.__name__,  self.__get_pk__())

    def save(self):
        self.session = Session()
        self.session.add(self)
        self.session.commit()


def string_field(max_length, null=False, *args, **kwargs):
    return Column(String(max_length), nullable=null, *args, **kwargs)

def int_field(null=False, *args, **kwargs):
    return Column(Integer(), nullable=null, *args, **kwargs)

def float_field(null=False, *args, **kwargs):
    return Column(Float(), nullable=null, *args, **kwargs)

def boolean_field(null=False, *args, **kwargs):
    return Column(Boolean(), nullable=null, *args, **kwargs)

def auto_field(class_name, *args, **kwargs):
    """ auto increment field. PK always true, class name has to be unique """
    return Column(
        Integer, Sequence(class_name + '_seq'), primary_key=True, *args, **kwargs
    )

def foreign_key(column, *args, **kwargs):
    return Column(Integer, ForeignKey(column), *args, **kwargs)
