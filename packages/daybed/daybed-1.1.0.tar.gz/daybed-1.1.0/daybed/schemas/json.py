from __future__ import absolute_import
import re
import json

from pyramid.i18n import TranslationString as _
import six
from colander import Sequence, null, Invalid, List, Mapping

from .base import registry, TypeField


__all__ = ['JSONField']


def parse_json(node, cstruct):
    if cstruct is null:
        return cstruct
    try:
        appstruct = cstruct
        if isinstance(cstruct, six.string_types):
            appstruct = json.loads(cstruct)
    except ValueError as e:
        raise Invalid(node, six.text_type(e), cstruct)
    return appstruct


class JSONType(Mapping):
    """A simple node type for JSON content."""
    def __init__(self, *args, **kwargs):
        kwargs['unknown'] = 'preserve'
        super(JSONType, self).__init__(*args, **kwargs)

    def deserialize(self, node, cstruct=null):
        appstruct = parse_json(node, cstruct)
        if not isinstance(appstruct, dict):
            # If JSON is not a dict, bypass ``Mapping``
            return appstruct
        return super(JSONType, self).deserialize(node, appstruct)


@registry.add('json')
class JSONField(TypeField):
    node = JSONType
    hint = _('A JSON value')


class JSONSequence(Sequence):
    """A sequence of items in JSON-like format"""
    def deserialize(self, node, cstruct, **kwargs):
        appstruct = parse_json(node, cstruct)
        return super(JSONSequence, self).deserialize(node, appstruct, **kwargs)


class JSONList(List):
    """Pure JSON or string, as serialized JSON or comma-separated values"""
    def deserialize(self, node, cstruct, **kwargs):
        try:
            appstruct = parse_json(node, cstruct)
        except Invalid:
            cstruct = re.sub(r'^\s*\[(.*)\]\s*', r'\1', cstruct)
            appstruct = re.split(r'\s*,\s*', cstruct)
        return super(JSONList, self).deserialize(node, appstruct, **kwargs)
