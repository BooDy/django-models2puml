from django.core.management.base import BaseCommand, CommandError
from models2puml.utils import validate_django_model, _render_class
from django.conf import settings


class Command(BaseCommand):
    help = 'Generate plantUML description of installed apps models'

    def add_arguments(self, parser):
        parser.add_argument('--apps', nargs="*", default="*", type=str,
                            help="Select the installed django apps to \
                            generate the plantUML schema from their models.\
                            Defaults to all installed apps")

        parser.add_argument('--output', nargs=1, default=None, type=str,
                            help="Path and name to a text file where the\
                            output of the command will be written to.\
                            Defaults to outputing to stdout.")

    def handle(self, *args, **options):

        apps = options['apps']
        if apps == '*':
            # load all installed apps from the django settings.
            self.stdout.write(self.style.WARNING('The output plantUML might \
                                                 not be rendered properly if \
                                                 the number of models is too \
                                                 big'))
            apps = settings.INSTALLED_APPS
        rel_fields = ['ForeignKey', 'ManyToManyField', 'OneToOneField']
        result = {}
        for app in apps:
            models_name = app + ".models"
            try:
                models_module = __import__(models_name, fromlist=["models"])
                result[app] = {}
            except ModuleNotFoundError:
                continue

            attributes = dir(models_module)
            for attr in attributes:
                try:
                    attrib = models_module.__getattribute__(attr)
                    if validate_django_model(attrib, models_name):
                        fields = attrib._meta.get_fields()
                        result[app][attr] = {'fields': {}, 'rel': []}
                        for field in fields:
                            result[app][attr]['fields'][field.name] = field.__class__.__name__
                            if field.__class__.__name__ in rel_fields:
                                result[app][attr]['rel'].append(
                                    field.remote_field.model.__name__
                                )
                except Exception as e:
                    raise CommandError('Model %s is fucked up: %s' % (attrib, e
                                                                      ))
        self.render_puml(result)

    def render_puml(self, apps):

        output = '@startuml'

        for app, models in apps.items():
            output += """\n package "%s" {""" % app

            for model, fields in models.items():
                output += _render_class(model, fields)

            output += """\n } """
        output += '\n@enduml'
        self.stdout.write(output)
