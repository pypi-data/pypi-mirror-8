from django.db import models
from django.core.exceptions import ValidationError
from django.core.serializers.pyyaml import DjangoSafeDumper
from south.modelsinspector import add_introspection_rules
import yaml


# Let South know how to handle our custom field type
add_introspection_rules([], ["^vr\.server\.fields\.YAMLDictField"])
add_introspection_rules([], ["^vr\.server\.fields\.YAMLListField"])


def validate_yaml_dict(value):
    if (value is not None and
        value != '' and
        not isinstance(value, dict)):

        raise ValidationError

class YAMLDictField(models.TextField):
    """
    YAMLDictField is a TextField that serializes and deserializes YAML dicts
    from the database.

    Based on https://github.com/datadesk/django-yamlfield, but goes one step
    further by ensuring that the data is a dict (or null), not just any valid
    yaml.
    """
    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(YAMLDictField, self).__init__(*args, **kwargs)
        self.validators.append(validate_yaml_dict)

    def to_python(self, value):
        """
        Convert our YAML string to a Python dict after we load it from the DB.
        Complain if it's not a dict.
        """
        if not value:
            return None

        # Seems like sometimes Django will pass a string into this function,
        # and other times a dict.  Pass out a dict either way.
        if isinstance(value, basestring):
            try:
                value = yaml.safe_load(value)
            except yaml.error.YAMLError as e:
                raise ValidationError(str(e))

        return value

    def get_db_prep_save(self, value, connection, prepared=False):
        """
        Convert our Python object to a string of YAML before we save.
        """
        if not value:
            return ""

        value = yaml.dump(value, Dumper=DjangoSafeDumper,
                          default_flow_style=False)
        return super(YAMLDictField, self).get_db_prep_save(value, connection)

    def value_from_object(self, obj):
        """
        Returns the value of this field in the given model instance.

        We need to override this so that the YAML comes out properly formatted
        in the admin widget.
        """
        value = getattr(obj, self.attname)
        if not value or value == "":
            return value
        return yaml.dump(value, Dumper=DjangoSafeDumper,
            default_flow_style=False)


def validate_yaml_list(value):
    if (value is not None and
        value != '' and
        not isinstance(value, (list, tuple))):

        raise ValidationError


class YAMLListField(models.TextField):
    """
    YAMLListField is a TextField that serializes and deserializes YAML lists
    from the database.

    Based on https://github.com/datadesk/django-yamlfield, but goes one step
    further by ensuring that the data is a list (or null), not just any valid
    yaml.
    """
    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(YAMLListField, self).__init__(*args, **kwargs)
        self.validators.append(validate_yaml_list)

    def to_python(self, value):
        """
        Convert our YAML string to a Python list after we load it from the DB.
        """
        if not value:
            return None

        # Seems like sometimes Django will pass a string into this function,
        # and other times a dict.  Pass out a dict either way.
        if isinstance(value, basestring):
            try:
                value = yaml.safe_load(value)
            except yaml.error.YAMLError as e:
                raise ValidationError(str(e))

        return value

    def get_db_prep_save(self, value, connection, prepared=False):
        """
        Convert our Python object to a string of YAML before we save.
        """
        if not value:
            return ""

        value = yaml.dump(value, Dumper=DjangoSafeDumper,
                          default_flow_style=False)
        return super(YAMLListField, self).get_db_prep_save(value, connection)

    def value_from_object(self, obj):
        """
        Returns the value of this field in the given model instance.

        We need to override this so that the YAML comes out properly formatted
        in the admin widget.
        """
        value = getattr(obj, self.attname)
        if not value or value == "":
            return value
        return yaml.dump(value, Dumper=DjangoSafeDumper,
            default_flow_style=False)
