from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class SubdomainLocalhostSiteMiddleware(MiddlewareMixin):
    """
    During debug you can go to:
        domainname.com.localhost/page/
    and it will interpret that as
        domainname.com/page/
    so that you can test domains without setting up some kind of weird local host thing.
    """

    def process_request(self, request):
        if settings.DEBUG:
            domain = request.get_host()
            if domain != 'localhost' and domain.endswith('localhost'):
                host = request.META["HTTP_HOST"] = '.'.join(domain.split('.')[:-1])
