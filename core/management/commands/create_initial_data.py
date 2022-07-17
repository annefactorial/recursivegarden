from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from core.models import User
from django.template.loader import render_to_string
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        for host in settings.ENABLED_DOMAINS:
            Site.objects.get_or_create(
                domain=host,
                name=host.capitalize(),
            )

        for name, email in [
            ('Anne Factorial', 'anne@recursivegarden.com'),
            ('David Factorial', 'david@lessboring.com'),
            ('Phoebe Factorial', 'phoebefactorial@gmail.com'),
            ('Daniel Factorial', 'danielfactorial@gmail.com'),
        ]:
            user, _ = User.objects.get_or_create(
                name=name, email=email,
                is_staff=True, is_superuser=True,
            )
            user.set_password('password')
            user.save()
            
