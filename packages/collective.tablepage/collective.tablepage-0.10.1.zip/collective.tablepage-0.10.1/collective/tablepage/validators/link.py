# -*- coding: utf-8 -*-

from zope.interface import implements
from collective.tablepage.interfaces import IFieldValidator
from collective.tablepage import tablepageMessageFactory as _


class ValidatorRequired(object):
    """Validate that some data has been submitted"""
    implements(IFieldValidator)

    def __init__(self, field):
        self.field = field

    def validate(self, configuration, data=None):
        if 'required' not in configuration.get('options', []):
            return None
        form = self.field.request.form
        field_id = configuration['id']
        if not form.get("external_%s" % field_id) and not form.get('internal_%s' % field_id) and not data:
            return _('error_field_required', default='The field "$name" is required',
                     mapping={'name': configuration.get('label', configuration['id']).decode('utf-8')})
