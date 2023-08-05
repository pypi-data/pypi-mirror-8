from __future__ import absolute_import
from functools import partial
from copy import deepcopy
import json
import datetime

import six
from colander import (
    SchemaNode, Mapping, Sequence, Length, String, null, Invalid
)
from pyramid.security import Authenticated, Everyone

from daybed.backends.exceptions import ModelNotFound
from daybed.permissions import PERMISSIONS_SET
from daybed.backends.exceptions import CredentialsNotFound
from . import registry, TypeFieldNode


class DefinitionSchema(SchemaNode):
    def __init__(self):
        super(DefinitionSchema, self).__init__(Mapping())
        self.add(SchemaNode(String(), name='title'))
        self.add(SchemaNode(String(), name='description'))
        self.add(SchemaNode(Sequence(), SchemaNode(TypeFieldNode()),
                            name='fields', validator=Length(min=1)))


class RecordSchema(SchemaNode):
    def __init__(self, definition):
        super(RecordSchema, self).__init__(Mapping())
        definition = deepcopy(definition)
        for field in definition['fields']:
            field['root'] = self
            fieldtype = field.pop('type')
            self.add(registry.validation(fieldtype, **field))


class RecordValidator(object):
    """A validator to check that a dictionnary matches the specified
    definition.
    """
    def __init__(self, definition):
        self.schema = RecordSchema(definition)

    def __call__(self, node, value):
        self.schema.deserialize(value)


def validate_against_schema(request, schema, data, field_name=None):
    try:
        data_pure = schema.deserialize(data)
        data_clean = post_serialize(data_pure)
        # Attach data_clean to request: see usage in views.
        request.data_clean = data_clean
    except Invalid as e:
        def output_error(error, recurse=False):
            # here we transform the errors we got from colander into cornice
            # errors
            for field, error in error.asdict().items():
                request.errors.add('body', field or field_name or '', error)
                if recurse:
                    map(output_error, e.children)
        output_error(e, True)


def post_serialize(data):
    """Returns the most agnostic version of specified data.
    (remove colander notions, datetimes in ISO, ...)
    """
    clean = dict()
    for k, v in data.items():
        if isinstance(v, (datetime.date, datetime.datetime)):
            clean[k] = v.isoformat()
        elif v is null:
            pass
        else:
            clean[k] = v
    return clean


def validator(request, schema):
    """Validates the request according to the given schema"""
    try:
        body = request.body.decode('utf-8')
        dictbody = json.loads(body) if body else {}
        validate_against_schema(request, schema, dictbody)
    except ValueError as e:
        request.errors.add('body', 'body', six.text_type(e))


#  Validates a request body according model definition schema.
definition_validator = partial(validator, schema=DefinitionSchema())


def record_validator(request):
    """Validates a request body according to its model definition.
    """
    model_id = request.matchdict['model_id']

    try:
        definition = request.db.get_model_definition(model_id)
        schema = RecordSchema(definition)
        validator(request, schema)
    except ModelNotFound:
        request.errors.add('path', 'modelname',
                           'Unknown model %s' % model_id)
        request.errors.status = 404


def model_validator(request):
    """Verify that the model is okay (that we have the right fields) and
    eventually populates it if there is a need to.
    """
    try:
        body = json.loads(request.body.decode('utf-8'))
    except ValueError:
        request.errors.add('body', 'json value error', "malformed body")
        return

    # Check the definition is valid.
    definition = body.get('definition')
    if not definition:
        request.errors.add('body', 'definition', 'definition is required')
    else:
        validate_against_schema(request, DefinitionSchema(), definition,
                                'definition')
    request.validated['definition'] = definition

    # Check that the records are valid according to the definition.
    records = body.get('records')
    request.validated['records'] = []
    if records:
        definition_schema = RecordSchema(definition)
        for record in records:
            validate_against_schema(request, definition_schema, record)
            request.validated['records'].append(record)


def permissions_validator(request):
    """Verify that the permissions defined in the request body are valid:
         - tokens exists
         - permission names are valid
    """
    try:
        body = json.loads(request.body.decode('utf-8'))
    except ValueError:
        request.errors.add('body', 'json value error', "malformed body")
        return

    request.validated['permissions'] = {}

    # Check the definition is valid.
    for credentials_id, permissions in six.iteritems(body):
        error = False
        strip_dash = lambda perm: perm.lstrip('-').lstrip('+').lower()
        perms = set([strip_dash(perm) for perm in permissions])
        if "all" in perms:
            perms = set(PERMISSIONS_SET)
        if not perms.issubset(PERMISSIONS_SET):
            request.errors.add('body', credentials_id,
                               'Invalid permissions: %s' %
                               ', '.join((perms - PERMISSIONS_SET)))
            error = True
        if credentials_id not in ("Authenticated", "Everyone"):
            if credentials_id not in (Authenticated, Everyone):
                try:
                    request.db.get_token(credentials_id)
                except CredentialsNotFound:
                    request.errors.add("body", credentials_id,
                                       "Credentials id couldn't be found.")
                    error = True
        else:
            credentials_id = credentials_id \
                .replace("Authenticated", Authenticated) \
                .replace("Everyone", Everyone)
        if not error:
            request.validated["permissions"][credentials_id] = permissions
