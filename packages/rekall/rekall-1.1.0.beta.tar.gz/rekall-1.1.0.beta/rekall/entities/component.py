# Rekall Memory Forensics
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

"""
Helper functions to make defining components nicer.

Exists solely to support rekall.entities.definitions.
"""
__author__ = "Adam Sindelar <adamsh@google.com>"

import collections
import operator

from rekall import registry


# DeclareComponent will ensure this namedtuple has a field for every type of
# component we define in rekall.entities.definitions. It's used as a
# high-performance container class by the Entity class.
ComponentContainer = collections.namedtuple("ComponentContainer", [])

# An empty instance (prototype) of ComponentContainer used for quickly
# instantiating entities.
CONTAINER_PROTOTYPE = ComponentContainer()


class TypeDescriptor(object):
    """Defines a type descriptor, which can coerce values into target type."""

    def __init__(self):
        pass

    def coerce(self, value):
        """Return value as this type or raise TypeError if not convertible."""
        return value

    def __repr__(self):
        return None

    def __unicode__(self):
        return repr(self)

    def __str__(self):
        return repr(self)


class ScalarDescriptor(object):
    """Take an instance of type and calls its constructor to coerce."""

    def __init__(self, type_cls):
        super(ScalarDescriptor, self).__init__()
        self.type_cls = type_cls

    def coerce(self, value):
        return self.type_cls(value)

    def __repr__(self):
        return "%s (scalar type)" % self.type_cls.__name__


class NoneDescriptor(TypeDescriptor):
    "NoneDescriptor doesn't care."

    def __init__(self):
        super(NoneDescriptor, self).__init__()

    def coerce(self, value):
        return value

    def __repr__(self):
        return "untyped (NoneDescriptor)"


class TypeNameDescriptor(TypeDescriptor):
    """Defined using type name instead of type class - can only validate."""

    def __init__(self, type_name):
        super(TypeNameDescriptor, self).__init__()
        self.type_name = type_name

    def coerce(self, value):
        if type(value).__name__ != self.type_name:
            raise TypeError("%s is not of type %s and cannot be coerced.",
                            value, self.type_name)

    def __repr__(self):
        return "\"%s\" (type-name type)" % self.type_name


class TupleDescriptor(TypeDescriptor):
    """Declared for tuple types; coerces each member to its respective type."""

    def __init__(self, tpl):
        super(TupleDescriptor, self).__init__()
        self.types = [TypeFactory(x) for x in tpl]

    def coerce(self, value):
        return tuple(self.types[i](x) for i, x in enumerate(value))

    def __repr__(self):
        return "(%s)" % ", ".join(self.types)


class ListDescriptor(TypeDescriptor):
    """Declared for nested types (e.g. list of ints)."""

    def __init__(self, member_type):
        super(ListDescriptor, self).__init__()
        self.member_type = TypeFactory(member_type)

    def coerce(self, value):
        return [self.member_type.coerce(x) for x in value]

    def __repr__(self):
        return "[%s] (list type)" % self.member_type


class EnumDescriptor(TypeDescriptor):
    """Defines an enum type for a component attribute."""

    def __init__(self, *args):
        super(EnumDescriptor, self).__init__()
        self.legal_values = args
        self.type_name = "str"

    def coerce(self, value):
        value = str(value)
        if value not in self.legal_values:
            raise TypeError("%s is not a valid value for enum %s",
                            value, self.legal_values)

        return value


def TypeFactory(type_desc):
    """Creates the appropriate TypeDescriptor or subclass instance.

    If given a type instance, will create TypeDescriptor (most common use).

    If given a string, will interpret is as name of class and create
    a TypeNameDescriptor.

    If given a set, will interpret it as enum and create EnumDescriptor.

    If given a tuple, will interpret as composite attribute and create a
    TupleDescriptor.

    If given a list, will interpret is as a nested type and create a
    ListDescriptor.
    """
    if isinstance(type_desc, TypeDescriptor):
        # Fall through for stuff defined explictly.
        return type_desc

    if isinstance(type_desc, type):
        return ScalarDescriptor(type_desc)

    if isinstance(type_desc, str):
        return TypeNameDescriptor(type_desc)

    if type_desc is None:
        return NoneDescriptor()

    if isinstance(type_desc, set):
        return EnumDescriptor(*type_desc)

    if isinstance(type_desc, tuple):
        return TupleDescriptor(type_desc)

    if isinstance(type_desc, list):
        return ListDescriptor(type_desc[0])

    raise TypeError("%s is not a valid type descriptor.", type_desc)


class Field(object):
    """Defines a component attribute.

    Arguments:

    name: name for the attribute - must be valid python property name.
    docstring: Arbitrary documentation string for this attribute.
    typedesc: The type descriptor. Must be instance of TypeDescriptor or valid
        argument for TypeFactory.
    """

    def __init__(self, name, typedesc, docstring):
        self.name = name
        self.typedesc = TypeFactory(typedesc)
        self.docstring = docstring

    def __unicode__(self):
        return repr(self)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Field(%s, type=%s)" % (self.name, self.typedesc)


class Component(object):
    # __slots__ = ("_contents", "_object_id")
    component_fields = None
    component_name = None
    component_docstring = None

    __abstract = True
    __metaclass__ = registry.MetaclassRegistry

    def __init__(self, *args, **kwargs):
        self._contents = list(args)
        for field in self.component_fields[len(args):]:
            self._contents.append(kwargs.pop(field.name, None))

        if kwargs:
            raise ValueError("Unknown attributes %s on component %s" % (
                kwargs, self.name))

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._contents[key]

        return getattr(self, key)


# pylint: disable=protected-access
def DeclareComponent(name, docstring, *fields):
    """Defines a new component."""

    # Subclass Component, overriding the component_* class variables.
    props = dict(
        # __slots__=(),
        component_fields=fields,
        component_name=name,
        component_docstring=docstring)

    for idx, field in enumerate(fields):
        props[field.name] = property(operator.itemgetter(idx))

    component_cls = type(name, (Component,), props)

    # Redefine ComponentContainer to add a field for the new component class.
    global ComponentContainer
    component_names = list(ComponentContainer._fields)
    component_names.append(name)
    ComponentContainer = collections.namedtuple("ComponentContainer",
                                                component_names)

    # Update the container prototype.
    global CONTAINER_PROTOTYPE
    CONTAINER_PROTOTYPE = ComponentContainer(*[None for _ in component_names])

    return component_cls
