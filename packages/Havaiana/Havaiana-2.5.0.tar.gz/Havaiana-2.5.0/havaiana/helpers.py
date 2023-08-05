import os

from inspect import getmembers
from wtforms import Form, TextField, SelectField

import ojota.sources

from ojota import Ojota, current_data_code


def get_ojota_children(package):
    hijos = []
    items = getmembers(package)
    for item in items:
        try:
            if item[0] not in ("Ojota", "OjotaHierarchy") and \
                    issubclass(item[1], Ojota):
                hijos.append(item)
        except TypeError:
            pass
    return hijos

def get_data_codes():
    path = ojota.sources._DATA_SOURCE
    dirs = [dir_ for dir_ in os.listdir(path)
            if os.path.isdir(os.path.join(path, dir_))]
    return ['Root'] + sorted(dirs)

def get_form(cls, form_data, update=False):
    class HavaianaForm(Form):
        pass
    fields = [cls.pk_field]
    if hasattr(form_data, "fields"):
        fields += form_data.fields
    if cls.required_fields is not None:
        fields = set(fields + list(cls.required_fields))
    for field in fields:
        text_field = TextField()
        setattr(HavaianaForm, field, text_field)
    for key, value in cls.relations.items():
        choices = [(obj.primary_key, obj) for obj in  value[0].all()]
        text = value[1].replace("_", "  ").capitalize()
        text_field = SelectField(text, choices=choices)
        setattr(HavaianaForm, key, text_field)
    if update:
        form = HavaianaForm(obj=form_data)
    else:
        form = HavaianaForm(form_data)
    return form


def with_data_code(f):
    def _inner(self, *args, **kwargs):
        current_data_code(self.data_code)
        return f(self, *args, **kwargs)
    return _inner
