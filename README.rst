==================
Django models2puml
==================

Django models to PlantUML is a Django application which provides a management command to generate
a PlantUML class diagram based on the install apps Django models.
For more information about the PlantUML tool and text format https://plantuml.com


Installation & usage
--------------------

1. to use the application first you need to install it in your environment using pip

pip install django_modesl2puml

2. Add the application to your settings INSTALLED_APPS::
    INSTALLED_APPS = [
        ...
        'django_models2puml',

    ]

3. Use the newly available management command using manage.py::

   ./manage.py generatepuml --apps <Installed app name(s)>

4. The output of the command is a plantUML text description of a class diagram of your installed apps models

