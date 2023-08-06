# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import smart_text
from django.utils.six import with_metaclass
from django.utils.translation import ugettext_lazy as _

from .forms import LatLongField as FormLatLongField


class LatLong(object):
    def __init__(self, latitude=0.0, longitude=0.0):
        self.latitude = Decimal(latitude)
        self.longitude = Decimal(longitude)

    @staticmethod
    def _equals_to_the_cent(a, b):
        return round(a, 6) == round(b, 6)

    @staticmethod
    def _no_equals_to_the_cent(a, b):
        return round(a, 6) != round(b, 6)

    def __repr__(self):
        return '<{}: {:.6f};{:.6f}>'.format(self.__class__.__name__, self.latitude, self.longitude)

    def __str__(self):
        return '{:.6f};{:.6f}'.format(self.latitude, self.longitude)

    def __eq__(self, other):
        return isinstance(other, LatLong) and (self._equals_to_the_cent(self.latitude, other.latitude) and
                                               self._equals_to_the_cent(self.longitude, other.longitude))

    def __ne__(self, other):
        return isinstance(other, LatLong) and (self._no_equals_to_the_cent(self.latitude, other.latitude) or
                                               self._no_equals_to_the_cent(self.longitude, other.longitude))


class LatLongField(with_metaclass(models.SubfieldBase, models.Field)):
    description = _('Geographic coordinate system fields')
    default_error_messages = {
        'invalid': _("'%(value)s' both values must be a decimal number or integer."),
        'invalid_separator': _("As the separator value '%(value)s' must be ';'"),
    }

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 24
        super(LatLongField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if value is None:
            return None
        elif not value:
            return LatLong()
        elif isinstance(value, LatLong):
            return value
        elif isinstance(value, (list, tuple)):
            return LatLong(latitude=value[0], longitude=value[1])
        else:
            args = value.split(';')

            if len(args) != 2:
                raise ValidationError(
                    self.error_messages['invalid_separator'], code='invalid', params={'value': value},
                )

            try:
                return LatLong(*args)
            except InvalidOperation:
                raise ValidationError(
                    self.error_messages['invalid'], code='invalid', params={'value': value},
                )

    def get_prep_value(self, value):
        value = super(LatLongField, self).get_prep_value(value)
        if value:
            return str(value)
        elif value is None:
            return None
        return str(LatLong())

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return smart_text(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': FormLatLongField,
        }
        defaults.update(kwargs)
        return super(LatLongField, self).formfield(**defaults)


try:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([], ["^treasuremap\.fields\.LatLongField"])
except ImportError:
    pass