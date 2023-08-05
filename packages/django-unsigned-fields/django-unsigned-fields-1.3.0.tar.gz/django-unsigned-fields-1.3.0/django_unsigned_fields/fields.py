from __future__ import unicode_literals

import django
from django.conf import settings
from django.core import exceptions
from django.db import connection as default_connection
from django.db.models import fields
from django.db.models.fields.related import (
    OneToOneField,
    ManyToManyField,
    add_lazy_relation,
    ReverseManyRelatedObjectsDescriptor,
    RECURSIVE_RELATIONSHIP_CONSTANT,
)
from django.utils.translation import ugettext as _
from django.utils.functional import curry

from django_unsigned_fields.compat import (
    six, create_many_to_many_intermediary_model,
)

KILOBYTES = 1024
MEGABYTES = 1024 * KILOBYTES
GIGABYTES = 1024 * MEGABYTES

REWARDS_IMAGE_MAX_UPLOAD_SIZE = 5 * MEGABYTES


class UnsignedManyToManyField(ManyToManyField):
    def __init__(self, *args, **kwargs):
        self.from_unsigned = kwargs.pop('from_unsigned', True)
        self.to_unsigned = kwargs.pop('to_unsigned', True)
        super(UnsignedManyToManyField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        # To support multiple relations to self, it's useful to have a non-None
        # related name on symmetrical relations for internal reasons. The
        # concept doesn't make a lot of sense externally ("you want me to
        # specify *what* on my non-reversible relation?!"), so we set it up
        # automatically. The funky name reduces the chance of an accidental
        # clash.
        if self.rel.symmetrical and (self.rel.to == "self" or self.rel.to == cls._meta.object_name):
            self.rel.related_name = "%s_rel_+" % name

        super(ManyToManyField, self).contribute_to_class(cls, name)

        # The intermediate m2m model is not auto created if:
        #  1) There is a manually specified intermediate, or
        #  2) The class owning the m2m field is abstract.
        #  3) The class owning the m2m field has been swapped out.
        if not self.rel.through and not cls._meta.abstract and not getattr(cls._meta, 'swapped', False):
            self.rel.through = create_many_to_many_intermediary_model(self, cls)

        # Add the descriptor for the m2m relation
        setattr(cls, self.name, ReverseManyRelatedObjectsDescriptor(self))

        # Set up the accessor for the m2m table name for the relation
        self.m2m_db_table = curry(self._get_m2m_db_table, cls._meta)

        # Populate some necessary rel arguments so that cross-app relations
        # work correctly.
        if isinstance(self.rel.through, six.string_types):
            def resolve_through_model(field, model, cls):
                field.rel.through = model
            add_lazy_relation(cls, self, self.rel.through, resolve_through_model)

    def deconstruct(self):
        name, path, args, kwargs = super(UnsignedManyToManyField, self).deconstruct()
        kwargs['to_unsigned'] = self.to_unsigned
        kwargs['from_unsigned'] = self.from_unsigned
        return name, path, args, kwargs


class UnsignedIntegerField(fields.IntegerField):
    def db_type(self, connection=None):
        connection = connection or default_connection
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
            return "integer UNSIGNED"
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            return 'integer'
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
            return 'bigint'
        else:
            raise NotImplementedError

    def get_internal_type(self):
        return "UnsignedIntegerField"

    def to_python(self, value):
        if value is None:
            return value
        try:
            return value
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                _("This value must be an unsigned integer."))


class UnsignedAutoField(fields.AutoField):
    def db_type(self, connection=None):
        connection = connection or default_connection
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
            return "integer UNSIGNED AUTO_INCREMENT"
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            return 'integer'
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
            return 'bigserial'
        else:
            raise NotImplementedError

    def get_internal_type(self):
        return "UnsignedAutoField"

    def to_python(self, value):
        if value is None:
            return value
        try:
            return value
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                _("This value must be a long integer."))


class UnsignedForeignKey(fields.related.ForeignKey):
    def db_type(self, connection=None):
        connection = connection or default_connection
        rel_field = self.rel.get_related_field()
        # next lines are the "bad tooth" in the original code:
        if (isinstance(rel_field, UnsignedAutoField) or
            (not connection.features.related_fields_match_type and
             isinstance(rel_field, UnsignedIntegerField))):
            # because it continues here in the django code:
            # return IntegerField().db_type()
            # thereby fixing any AutoField as IntegerField
            return UnsignedIntegerField().db_type()
        return rel_field.db_type(connection)


class UnsignedOneToOneField(UnsignedForeignKey, OneToOneField):
    """
    If you use subclass model, you might need to name
    the `ptr` field explicitly. This is the field type you
    might want to use. Here is an example:

    class Base(models.Model):
        title = models.CharField(max_length=40, verbose_name='Title')

    class Concrete(Base):
        base_ptr = fields.BigOneToOneField(Base)
        ext = models.CharField(max_length=12, null=True, verbose_name='Ext')
    """
    pass


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        rules=[],
        patterns=[r'^django_unsigned_fields\.fields\.UnsignedIntegerField$'],
    )
    add_introspection_rules(
        rules=[],
        patterns=[r'^django_unsigned_fields\.fields\.UnsignedAutoField$'],
    )
    add_introspection_rules(
        rules=[],
        patterns=[r'^django_unsigned_fields\.fields\.UnsignedForeignKey$'],
    )
    add_introspection_rules(
        rules=[],
        patterns=[r'^django_unsigned_fields\.fields\.UnsignedOneToOneField$'],
    )
    add_introspection_rules(
        rules=[],
        patterns=[r'^django_unsigned_fields\.fields\.UnsignedManyToManyField$'],
    )
except ImportError:
    pass
