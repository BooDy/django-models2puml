import inspect
from django.db import models

def validate_django_model(model, app):
    return inspect.isclass(model) and ( issubclass(model, models.Model) and
                            model.__module__ == app)

def get_model_parent(model):
    tree = inspect.getclasstree(inspect.getmro(model), unique=True)


def _render_class(model, data):

    output = """\n class %s {""" % model

    for field_name, field_type in data['fields'].items():

        output += """\n %s %s""" % (field_name, field_type)

    output += """\n } """

    return output
