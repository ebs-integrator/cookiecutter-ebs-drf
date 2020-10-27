{% endraw %}
import os

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Rebuild indexes'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)
        parser.add_argument('fields', type=str)

    def handle(self, *args, **options):
        model_name = options['model']
        model_name_lower = model_name.lower()
        fields = ''
        for field in options['fields'].split(','):
            fields += '\'' + field + '\','
        returned_fields = fields + '\'id\','
        model_plural_name = model_name + 's'
        model_name_plural_lower = model_plural_name.lower()
        model_directory = 'apps/' + model_name_plural_lower
        if not os.path.isdir('apps/' + model_name_plural_lower):
            os.makedirs('apps/' + model_name_plural_lower)
        with open('apps/common/management/commands/default_serializer.txt', 'r') as f:
            data = f.read()
            data_for_serializer = data.replace('{{model_name}}', model_name)
            data_for_serializer = data_for_serializer.replace('{{model_plural_name}}', model_plural_name)
            data_for_serializer = data_for_serializer.replace('{{fields}}', fields)
            data_for_serializer = data_for_serializer.replace('{{returned_fields}}', returned_fields)
            data_for_serializer = data_for_serializer.replace('{{model_name_plural_lower}}', model_name_plural_lower)
            with open(model_directory + '/serializers.py', 'w') as f:
                f.write(data_for_serializer)
        self.stdout.write(self.style.SUCCESS('Serializer was successfully created'))

        fields_for_model = ''
        for field in options['fields'].split(','):
            fields_for_model += '\t' + field + ' = models' + '\n'
        with open('apps/common/management/commands/default_model.txt', 'r') as f:
            data = f.read()
            data_for_view = data.replace('{{model_name}}', model_name)
            data_for_view = data_for_view.replace('{{fields_for_model}}', fields_for_model)
            with open(model_directory + '/models.py', 'w') as f:
                f.write(data_for_view)
        self.stdout.write(self.style.SUCCESS('Model was successfully created'))
        with open('apps/common/management/commands/default_view.txt', 'r') as f:
            data = f.read()
            data_for_model = data.replace('{{model_name}}', model_name)
            data_for_model = data_for_model.replace('{{model_plural_name}}', model_plural_name)
            data_for_model = data_for_model.replace('{{fields}}', fields)
            data_for_model = data_for_model.replace('{{returned_fields}}', returned_fields)
            data_for_model = data_for_model.replace('{{model_name_plural_lower}}', model_name_plural_lower)
            with open(model_directory + '/views.py', 'w') as f:
                f.write(data_for_model)
        self.stdout.write(self.style.SUCCESS('View was successfully created'))
        with open('apps/common/management/commands/default_urls.txt', 'r') as f:
            data = f.read()
            data_for_model = data.replace('{{model_name}}', model_name)
            data_for_model = data_for_model.replace('{{model_plural_name}}', model_plural_name)
            data_for_model = data_for_model.replace('{{model_name_lower}}', model_name_lower)
            data_for_model = data_for_model.replace('{{model_name_plural_lower}}', model_name_plural_lower)
            with open(model_directory + '/urls.py', 'w') as f:
                f.write(data_for_model)
        self.stdout.write(self.style.SUCCESS('Urls was successfully created'))
        open(model_directory + '/helper.py', 'a').close()
        self.stdout.write(self.style.SUCCESS('Helper was successfully created'))
        open(model_directory + '/tests.py', 'a').close()
        self.stdout.write(self.style.SUCCESS('tests was successfully created'))
        open(model_directory + '/__init__.py', 'a').close()
{% endraw %}