import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from _generate_view import generate_view

class Command(BaseCommand):
    args = '<view_name view_name ...>'
    help = 'Creates a new view, adds the styles, and imports it'

    def handle(self, *args, **options):
        if hasattr(settings, 'BASE_DIR'):
            dir = settings.BASE_DIR
        else:
            dir = '.'
        for view_name in args:
            generate_view(dir + os.sep + 'assets', view_name)
            self.stdout.write('Successfully initialized view "%s"' % view_name)
