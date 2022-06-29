from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        nginx_conf = render_to_string(
            'nginx.conf', {
                'hosts': settings.ENABLED_DOMAINS,
                'BASE_DIR': str(settings.BASE_DIR).rstrip('/') + '/',
            })

        self.stdout.write(nginx_conf)
