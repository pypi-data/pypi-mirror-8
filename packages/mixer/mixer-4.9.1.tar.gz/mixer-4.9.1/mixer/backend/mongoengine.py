""" Support for Mongoengine ODM.

.. note:: Support for Mongoengine_ is in early development.

::

    from mixer.backend.mongoengine import mixer

    class User(Document):
        created_at = DateTimeField(default=datetime.datetime.now)
        email = EmailField(required=True)
        first_name = StringField(max_length=50)
        last_name = StringField(max_length=50)

    class Post(Document):
        title = StringField(max_length=120, required=True)
        author = ReferenceField(User)
        tags = ListField(StringField(max_length=30))

    post = mixer.blend(Post, author__username='foo')

"""
from __future__ import absolute_import

import datetime
import decimal

from bson import ObjectId
from mongoengine import (
    BooleanField,
    DateTimeField,
    DecimalField,
    Document,
    EmailField,
    EmbeddedDocumentField,
    FloatField,
    GenericReferenceField,
    GeoPointField,
    IntField,
    LineStringField,
    ListField,
    ObjectIdField,
    PointField,
    PolygonField,
    ReferenceField,
    StringField,
    URLField,
    UUIDField,
)

from .. import mix_types as t, generators as g, fakers as f
from ..main import (
    SKIP_VALUE, TypeMixer as BaseTypeMixer, GenFactory as BaseFactory,
    Mixer as BaseMixer,
)


def get_objectid(**kwargs):
    """ Create a new ObjectId instance.

    :return ObjectId:

    """
    return ObjectId()


def get_pointfield(**kwargs):
    """ Get a Point structure.

    :return dict:

    """
    return dict(type='Point', coordinates=f.get_coordinates())


def get_linestring(length=5, **kwargs):
    """ Get a LineString structure.

    :return dict:

    """
    return dict(
        type='LineString',
        coordinates=[f.get_coordinates() for _ in range(length)])


def get_polygon(length=5, **kwargs):
    """ Get a Poligon structure.

    :return dict:

    """
    lines = []
    for _ in range(length):
        line = get_linestring()['coordinates']
        if lines:
            line.insert(0, lines[-1][-1])

        lines.append(line)

    if lines:
        lines[0].insert(0, lines[-1][-1])

    return dict(type='Poligon', coordinates=lines)


def get_generic_reference(_typemixer=None, **params):
    """ Choose a GenericRelation. """
    meta = type(_typemixer)
    scheme = g.get_choice([
        m for (_, m, _, _) in meta.mixers.keys()
        if issubclass(m, Document) and m is not _typemixer._TypeMixer__scheme # noqa
    ])

    return TypeMixer(scheme, mixer=_typemixer._TypeMixer__mixer,
                     factory=_typemixer._TypeMixer__factory,
                     fake=_typemixer._TypeMixer__fake).blend(**params)


class GenFactory(BaseFactory):

    """ Map a mongoengine classes to simple types. """

    types = {
        BooleanField: bool,
        DateTimeField: datetime.datetime,
        DecimalField: decimal.Decimal,
        EmailField: t.EmailString,
        FloatField: float,
        IntField: int,
        StringField: str,
        URLField: t.URL,
        UUIDField: t.UUID,
    }

    generators = {
        GenericReferenceField: get_generic_reference,
        GeoPointField: f.get_coordinates,
        LineStringField: get_linestring,
        ObjectIdField: get_objectid,
        PointField: get_pointfield,
        PolygonField: get_polygon,
    }


class TypeMixer(BaseTypeMixer):

    """ TypeMixer for Mongoengine. """

    factory = GenFactory

    def make_generator(self, me_field, field_name=None, fake=None, args=None, kwargs=None): # noqa
        """ Make values generator for field.

        :param me_field: Mongoengine field's instance
        :param field_name: Field name
        :param fake: Force fake data

        :return generator:

        """
        ftype = type(me_field)
        args = [] if args is None else args
        kwargs = {} if kwargs is None else kwargs

        if me_field.choices:
            if isinstance(me_field.choices[0], tuple):
                choices, _ = list(zip(*me_field.choices))
            else:
                choices = list(me_field.choices)

            return g.gen_choice(choices)

        if ftype is StringField:
            kwargs['length'] = me_field.max_length

        elif ftype is ListField:
            gen = self.make_generator(me_field.field, kwargs=kwargs)
            return g.loop(lambda: [next(gen) for _ in range(3)])()

        elif isinstance(me_field, (EmbeddedDocumentField, ReferenceField)):
            ftype = me_field.document_type

        elif ftype is GenericReferenceField:
            kwargs.update({'_typemixer': self})

        elif ftype is DecimalField:
            sign, (ii,), dd = me_field.precision.as_tuple()
            kwargs['d'] = abs(dd)
            kwargs['positive'] = not sign
            kwargs['i'] = ii + 1

        return super(TypeMixer, self).make_generator(
            ftype, field_name=field_name, fake=fake, args=args, kwargs=kwargs)

    @staticmethod
    def get_default(field):
        """ Get default value from field.

        :return value: A default value or NO_VALUE

        """
        if not field.scheme.default:
            return SKIP_VALUE

        if callable(field.scheme.default):
            return field.scheme.default()

        return field.scheme.default

    @staticmethod
    def is_unique(field):
        """ Return True is field's value should be a unique.

        :return bool:

        """
        return field.scheme.unique

    @staticmethod
    def is_required(field):
        """ Return True is field's value should be defined.

        :return bool:

        """
        if isinstance(field.scheme, ReferenceField):
            return True

        return field.scheme.required or isinstance(field.scheme, ObjectIdField)

    def gen_select(self, field_name, select):
        """ Select related document from mongo. """
        field = self.__fields.get(field_name)
        if not field:
            return super(TypeMixer, self).gen_select(field_name, select)

        return field.name, field.scheme.document_type.objects.filter(**select.params).first()

    def guard(self, *args, **kwargs):
        """ Ensure for an objects are exist in DB. """
        qs = self.__scheme.objects(*args, **kwargs)
        count = len(qs)
        if count == 1:
            return qs[0]
        return qs

    def reload(self, obj):
        """ Reload object from storage. """
        return self.__scheme.get(id=obj.id)

    def __load_fields(self):
        for fname, field in self.__scheme._fields.items():

            yield fname, t.Field(field, fname)


class Mixer(BaseMixer):

    """ Mixer class for mongoengine.

    Default mixer (desnt save a generated instances to db)
    ::

        from mixer.backend.mongoengine import mixer

        user = mixer.blend(User)

    You can initialize the Mixer by manual:
    ::
        from mixer.backend.mongoengine import Mixer

        mixer = Mixer(commit=True)
        user = mixer.blend(User)

    """

    type_mixer_cls = TypeMixer

    def __init__(self, commit=True, **params):
        """ Initialize the Mongoengine Mixer.

        :param fake: (True) Generate fake data instead of random data.
        :param commit: (True) Save object to Mongo DB.

        """
        super(Mixer, self).__init__(**params)
        self.params['commit'] = commit

    def postprocess(self, target):
        """ Save instance to DB.

        :return instance:

        """
        if self.params.get('commit') and isinstance(target, Document):
            target.save()

        return target


mixer = Mixer()


# pylama:ignore=E1120
