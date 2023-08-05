# -*- coding: utf-8 -*-
"""The :class:`Schema` class, including its metaclass and options (class Meta)."""
from __future__ import absolute_import

import copy
import datetime as dt
import json
import types
import uuid
import warnings
from collections import namedtuple
from functools import partial

from marshmallow import base, fields, utils, class_registry
from marshmallow.compat import (with_metaclass, iteritems, text_type,
                                binary_type, OrderedDict)
from marshmallow.orderedset import OrderedSet


#: Return type of :meth:`Schema.dump`
MarshalResult = namedtuple('MarshalResult', ['data', 'errors'])
#: Return type of :meth:`Schema.load`
UnmarshalResult = namedtuple('UnmarshalResult', ['data', 'errors'])

def _get_fields(attrs, field_class, pop=False):
    """Get fields from a class, sorted by creation index.

    :param attrs: Mapping of class attributes
    :param type field_class: Base field class
    :param bool pop: Remove matching fields
    """
    getter = getattr(attrs, 'pop' if pop else 'get')
    return sorted(
        [
            (field_name, getter(field_name))
            for field_name, field_value in list(iteritems(attrs))
            if utils.is_instance_or_subclass(field_value, field_class)
        ],
        key=lambda pair: pair[1]._creation_index,
    )

# This function allows Schemas to inherit from non-Schema classes and ensures
#   inheritance according to the MRO
def _get_fields_by_mro(klass, field_class):
    """Collect fields from a class, following its method resolution order. The
    class itself is excluded from the search; only its parents are checked. Get
    fields from ``_declared_fields`` if available, else use ``__dict__``.

    :param type klass: Class whose fields to retrieve
    :param type field_class: Base field class
    """
    return sum(
        (
            _get_fields(
                getattr(base, '_declared_fields', base.__dict__),
                field_class
            )
            for base in klass.mro()[:0:-1]
        ),
        [],
    )


class SchemaMeta(type):
    """Metaclass for the Schema class. Binds the declared fields to
    a ``_declared_fields`` attribute, which is a dictionary mapping attribute
    names to field objects.
    """

    def __new__(mcs, name, bases, attrs):
        fields = _get_fields(attrs, base.FieldABC, pop=True)
        klass = super(SchemaMeta, mcs).__new__(mcs, name, bases, attrs)
        fields = _get_fields_by_mro(klass, base.FieldABC) + fields
        klass._declared_fields = OrderedDict(fields)
        class_registry.register(name, klass)
        return klass


class SchemaOpts(object):
    """class Meta options for the :class:`Schema`. Defines defaults."""

    def __init__(self, meta):
        self.fields = getattr(meta, 'fields', ())
        if not isinstance(self.fields, (list, tuple)):
            raise ValueError("`fields` option must be a list or tuple.")
        self.additional = getattr(meta, 'additional', ())
        if not isinstance(self.additional, (list, tuple)):
            raise ValueError("`additional` option must be a list or tuple.")
        if self.fields and self.additional:
            raise ValueError("Cannot set both `fields` and `additional` options"
                            " for the same Schema.")
        self.exclude = getattr(meta, 'exclude', ())
        if not isinstance(self.exclude, (list, tuple)):
            raise ValueError("`exclude` must be a list or tuple.")
        self.strict = getattr(meta, 'strict', False)
        self.dateformat = getattr(meta, 'dateformat', None)
        self.json_module = getattr(meta, 'json_module', json)


class BaseSchema(base.SchemaABC):
    """Base schema class with which to define custom schemas.

    Example usage:

    .. code-block:: python

        from datetime import datetime
        from marshmallow import Schema, fields

        class Person(object):
            def __init__(self, name):
                self.name = name
                self.date_born = datetime.now()

        class PersonSchema(Schema):
            name = fields.String()
            date_born = fields.DateTime()

        # Or, equivalently
        class PersonSchema2(Schema):
            class Meta:
                fields = ("name", "date_born")

        person = Person("Guido van Rossum")
        schema = PersonSchema()
        data, errors = schema.dump(person)
        data  # OrderedDict([('name', u'Guido van Rossum'),
              #              ('date_born', '2014-08-19T21:06:10.620408')])

    :param obj: The object or collection of objects to be serialized. NOTE: This
        parameter is deprecated. Pass the object to the :meth:`dump` method
        instead.
    :param dict extra: A dict of extra attributes to bind to the serialized result.
    :param tuple only: A list or tuple of fields to serialize. If ``None``, all
        fields will be serialized.
    :param tuple exclude: A list or tuple of fields to exclude from the
        serialized result.
    :param str prefix: Optional prefix that will be prepended to all the
        serialized field names.
    :param bool strict: If ``True``, raise errors if invalid data are passed in
        instead of failing silently and storing the errors.
    :param bool many: Should be set to ``True`` if ``obj`` is a collection
        so that the object will be serialized to a list.
    :param dict context: Optional context passed to :class:`fields.Method` and
        :class:`fields.Function` fields.
    """
    TYPE_MAPPING = {
        text_type: fields.String,
        binary_type: fields.String,
        dt.datetime: fields.DateTime,
        float: fields.Float,
        bool: fields.Boolean,
        tuple: fields.Raw,
        list: fields.Raw,
        set: fields.Raw,
        int: fields.Integer,
        uuid.UUID: fields.UUID,
        dt.time: fields.Time,
        dt.date: fields.Date,
        dt.timedelta: fields.TimeDelta,
    }

    OPTIONS_CLASS = SchemaOpts

    #: Custom error handler function. May be ``None``.
    __error_handler__ = None

    #  NOTE: The below class attributes must initially be ``None`` so that
    #  every subclass references a different list of functions

    #: List of registered post-processing functions.
    __data_handlers__ = None
    #: List of registered schema-level validation functions.
    __validators__ = None
    #: List of registered pre-processing functions.
    __preprocessors__ = None

    class Meta(object):
        """Options object for a Schema.

        Example usage: ::

            class Meta:
                fields = ("id", "email", "date_created")
                exclude = ("password", "secret_attribute")

        Available options:

        - ``fields``: Tuple or list of fields to include in the serialized result.
        - ``additional``: Tuple or list of fields to include *in addition* to the
            explicitly declared fields. ``additional`` and ``fields`` are
            mutually-exclusive options.
        - ``exclude``: Tuple or list of fields to exclude in the serialized result.
        - ``dateformat``: Date format for all DateTime fields that do not have their
            date format explicitly specified.
        - ``strict``: If ``True``, raise errors during marshalling rather than
            storing them.
        - ``json_module``: JSON module to use for `loads` and `dumps`.
            Defaults to the ``json`` module in the stdlib.
        """
        pass

    def __init__(self, obj=None, extra=None, only=None,
                exclude=None, prefix='', strict=False, many=False,
                context=None):
        # copy declared fields from metaclass
        self.declared_fields = copy.deepcopy(self._declared_fields)
        #: Dictionary mapping field_names -> :class:`Field` objects
        self.fields = OrderedDict()
        self._data = None  # the cached, serialized data
        self.many = many
        self.opts = self.OPTIONS_CLASS(self.Meta)
        self.only = only or ()
        self.exclude = exclude or ()
        self.prefix = prefix
        self.strict = strict or self.opts.strict
        #: Callable marshalling object
        self._marshal = fields.Marshaller(
            prefix=self.prefix
        )
        #: Callable unmarshalling object
        self._unmarshal = fields.Unmarshaller()
        self.extra = extra
        self.context = context or {}
        self._update_fields()

        # For backwards compatibility, allow object to be passed in.
        self.obj = obj
        self._data = None
        # If object is passed in, marshal it immediately so that errors are stored
        if self.obj is not None:
            warnings.warn('Serializing objects in the Schema constructor is a '
                          'deprecated API. Use the Schema.dump method instead.',
                          category=DeprecationWarning)
            self._update_fields(self.obj)
            self._update_data()
        else:
            self._update_fields()

    def __repr__(self):
        return '<{ClassName}(many={self.many}, strict={self.strict})>'.format(
            ClassName=self.__class__.__name__, self=self
        )

    def _postprocess(self, data, obj):
        if self.extra:
            if self.many:
                for each in data:
                    each.update(self.extra)
            else:
                data.update(self.extra)
        if self._marshal.errors and callable(self.__error_handler__):
            self.__error_handler__(self._marshal.errors, obj)

        # invoke registered callbacks
        # NOTE: these callbacks will mutate the data
        if self.__data_handlers__:
            for callback in self.__data_handlers__:
                if callable(callback):
                    data = callback(self, data, obj)
        return data

    ##### Handler decorators #####

    @classmethod
    def error_handler(cls, func):
        """Decorator that registers an error handler function for the schema.
        The function receives the :class:`Schema` instance, a dictionary of errors,
        and the serialized object (if serializing data) or data dictionary (if
        deserializing data) as arguments.

        Example: ::

            class UserSchema(Schema):
                email = fields.Email()

            @UserSchema.error_handler
            def handle_errors(schema, errors, obj):
                raise ValueError('An error occurred while marshalling {}'.format(obj))

            user = User(email='invalid')
            UserSchema().dump(user)  # => raises ValueError
            UserSchema().load({'email': 'bademail'})  # raises ValueError

        .. versionadded:: 0.7.0

        """
        cls.__error_handler__ = func
        return func

    @classmethod
    def data_handler(cls, func):
        """Decorator that registers a post-processing function.
        The function receives the :class:`Schema` instance, the serialized
        data, and the original object as arguments and should return the
        processed data.

        Example: ::

            class UserSchema(Schema):
                name = fields.String()

            @UserSchema.data_handler
            def add_surname(schema, data, obj):
                data['surname'] = data['name'].split()[1]
                return data

        .. note::

            You can register multiple handler functions for the same schema.

        .. versionadded:: 0.7.0

        """
        cls.__data_handlers__ = cls.__data_handlers__ or []
        cls.__data_handlers__.append(func)
        return func

    @classmethod
    def validator(cls, func):
        """Decorator that registers a schema validation function to be applied during
        deserialization. The function receives the :class:`Schema` instance and the
        input data as arguments and should return ``False`` if validation fails.

        Example: ::

            class NumberSchema(Schema):
                field_a = fields.Integer()
                field_b = fields.Integer()

            @NumberSchema.validator
            def validate_numbers(schama, input_data):
                return input_data['field_b'] > input_data['field_a']

        .. note::

            You can register multiple validators for the same schema.

        .. versionadded:: 1.0

        """
        cls.__validators__ = cls.__validators__ or []
        cls.__validators__.append(func)
        return func

    @classmethod
    def preprocessor(cls, func):
        """Decorator that registers a preprocessing function to be applied during
        deserialization. The function receives the :class:`Schema` instance and the
        input data as arguments and should return the modified dictionary of data.

        Example: ::

            class NumberSchema(Schema):
                field_a = fields.Integer()
                field_b = fields.Integer()

            @NumberSchema.preprocessor
            def add_to_field_a(schama, input_data):
                input_data['field_a'] += 1
                return input_data

        .. note::

            You can register multiple preprocessors for the same schema.

        .. versionadded:: 1.0

        """
        cls.__preprocessors__ = cls.__preprocessors__ or []
        cls.__preprocessors__.append(func)
        return func

    ##### Serialization/Deserialization API #####

    def dump(self, obj):
        """Serialize an object to native Python data types according to this
        Schema's fields.

        :param obj: The object to serialize.
        :return: A tuple of the form (``data``, ``errors``)
        :rtype: `MarshalResult`, a `collections.namedtuple`

        .. versionadded:: 1.0.0
        """
        if not self.many and utils.is_collection(obj) and not utils.is_keyed_tuple(obj):
            warnings.warn('Implicit collection handling is deprecated. Set '
                            'many=True to serialize a collection.',
                            category=DeprecationWarning)
        if isinstance(obj, types.GeneratorType):
            obj = list(obj)
        self._update_fields(obj)
        preresult = self._marshal(
            obj,
            self.fields,
            many=self.many,
            strict=self.strict
        )
        result = self._postprocess(preresult, obj=obj)
        errors = self._marshal.errors
        return MarshalResult(result, errors)

    def dumps(self, obj, *args, **kwargs):
        """Same as :meth:`dump`, except return a JSON-encoded string.

        :param str json_data: A JSON string of the data to deserialize.
        :return: A tuple of the form (``data``, ``errors``)
        :rtype: `MarshalResult`, a `collections.namedtuple`

        .. versionadded:: 1.0.0
        """
        deserialized, errors = self.dump(obj)
        ret = self.opts.json_module.dumps(deserialized, *args, **kwargs)
        # # On Python 2, json.dumps returns bytestrings
        # # On Python 3, json.dumps returns unicode
        # # Ensure that a bytestring is returned
        if isinstance(ret, text_type):
            ret = bytes(ret.encode('utf-8'))
        return MarshalResult(ret, errors)

    def load(self, data):
        """Deserialize a data structure to an object defined by this Schema's
        fields and :meth:`make_object`.

        :param dict data: The data to deserialize.
        :return: A tuple of the form (``data``, ``errors``)
        :rtype: `UnmarshalResult`, a `collections.namedtuple`

        .. versionadded:: 1.0.0
        """
        # Bind self as the first argument of validators and preprocessors
        if self.__validators__:
            validators = [partial(func, self)
                         for func in self.__validators__]
        else:
            validators = []
        if self.__preprocessors__:
            preprocessors = [partial(func, self)
                            for func in self.__preprocessors__]
        else:
            preprocessors = []
        result = self._unmarshal(
            data,
            self.fields,
            many=self.many,
            strict=self.strict,
            validators=validators,
            preprocess=preprocessors,
            postprocess=[self.make_object]
        )
        errors = self._unmarshal.errors
        if self._unmarshal.errors and callable(self.__error_handler__):
            self.__error_handler__(self._unmarshal.errors, data)
        return UnmarshalResult(data=result, errors=errors)

    def loads(self, json_data, *args, **kwargs):
        """Same as :meth:`load`, except it takes a JSON string as input.

        :param str json_data: A JSON string of the data to deserialize.
        :return: A tuple of the form (``data``, ``errors``)
        :rtype: `UnmarshalResult`, a `collections.namedtuple`

        .. versionadded:: 1.0.0
        """
        return self.load(self.opts.json_module.loads(json_data, *args, **kwargs))

    def make_object(self, data):
        """Override-able method that defines how to create the final deserialization
        output. Defaults to noop (i.e. just return ``data`` as is).

        :param dict data: The deserialized data.

        .. versionadded:: 1.0.0
        """
        return data

    ##### Legacy API #####

    @property
    def data(self):
        """The serialized data as an :class:`OrderedDict`.

        .. deprecated:: 1.0.0
            Use the return value of `dump` instead.
        """
        warnings.warn('Accessing data through Schema.data is deprecated. '
                      'Use the return value of Schema.dump instead.',
                      category=DeprecationWarning)
        if not self._data:
            self._update_data()
        return self._data

    @property
    def errors(self):
        """Dictionary of errors raised during serialization.

        .. deprecated:: 1.0.0
            Use the return value of `load` instead.
        """
        return self._marshal.errors

    def _update_data(self):
        if not self._data:
            self._data = self.dump(self.obj).data
        return self._data

    ##### Private Helpers #####

    def _update_fields(self, obj=None):
        """Update fields based on the passed in object."""
        # if only __init__ param is specified, only return those fields
        if self.only:
            ret = self.__filter_fields(self.only, obj)
            self.__set_field_attrs(ret)
            self.fields = ret
            return self.fields

        if self.opts.fields:
            # Return only fields specified in fields option
            field_names = OrderedSet(self.opts.fields)
        elif self.opts.additional:
            # Return declared fields + additional fields
            field_names = (OrderedSet(self.declared_fields.keys()) |
                            OrderedSet(self.opts.additional))
        else:
            field_names = OrderedSet(self.declared_fields.keys())

        # If "exclude" option or param is specified, remove those fields
        excludes = set(self.opts.exclude) | set(self.exclude)
        if excludes:
            field_names = field_names - excludes
        ret = self.__filter_fields(field_names, obj)
        # Set parents
        self.__set_field_attrs(ret)
        self.fields = ret
        return self.fields

    def __set_field_attrs(self, fields_dict):
        """Set the parents of all field objects in fields_dict to self, and
        set the dateformat specified in ``class Meta``, if necessary.
        """
        for field_name, field_obj in iteritems(fields_dict):
            if not field_obj.parent:
                field_obj.parent = self
            if not field_obj.name:
                field_obj.name = field_name
            if isinstance(field_obj, fields.DateTime):
                if field_obj.dateformat is None:
                    field_obj.dateformat = self.opts.dateformat
        return fields_dict

    def __filter_fields(self, field_names, obj):
        """Return only those field_name:field_obj pairs specified by
        ``field_names``.

        :param set field_names: Field names to include in the final
            return dictionary.
        :returns: An OrderedDict of field_name:field_obj pairs.
        """
        # Convert obj to a dict
        obj_marshallable = utils.to_marshallable_type(obj,
            field_names=field_names)
        if obj_marshallable and self.many:
            try:  # Homogeneous collection
                obj_prototype = obj_marshallable[0]
            except IndexError:  # Nothing to serialize
                return self.declared_fields
            obj_dict = utils.to_marshallable_type(obj_prototype,
                field_names=field_names)
        else:
            obj_dict = obj_marshallable
        ret = OrderedDict()
        for key in field_names:
            if key in self.declared_fields:
                ret[key] = self.declared_fields[key]
            else:
                if obj_dict:
                    try:
                        attribute_type = type(obj_dict[key])
                    except KeyError:
                        raise AttributeError(
                            '"{0}" is not a valid field for {1}.'.format(key, obj))
                    field_obj = self.TYPE_MAPPING.get(attribute_type, fields.Field)()
                else:  # Object is None
                    field_obj = fields.Field()
                # map key -> field (default to Raw)
                ret[key] = field_obj
        return ret


class Schema(with_metaclass(SchemaMeta, BaseSchema)):
    __doc__ = BaseSchema.__doc__

Serializer = Schema
