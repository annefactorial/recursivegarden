from django.test import TestCase
from functools import wraps
from django.test.utils import override_settings
from django.urls import reverse


def with_params(params):
    """Decorates a test case to run it as a set of subtests."""

    def decorator(func):
        @wraps(func)
        def wrapped(self):
            for param in params:
                with self.subTest(**param):
                    func(self, **param)
        return wrapped
    return decorator


class RoomViewTemplateTest(TestCase):
    '''
    Test different combinations of incoming http hosts mapping to different templates
    '''
    @with_params([
        dict(
            root_host='localhost',
            incoming_host='localhost',
            incoming_path='path/to/',
            result_template_name='localhost/path/to/index.html'
        ),
        dict(
            root_host='localhost',
            incoming_host='localhost',
            incoming_path='path/to/',
            result_template_name='localhost/path/to/index.html'
        ),
        dict(
            root_host='recursivegarden.com',
            incoming_host='recursivegarden.com',
            incoming_path='/',
            result_template_name='recursivegarden.com/index.html'
        ),
        dict(
            root_host='recursivegarden.com',
            incoming_host='recursivegarden.com',
            incoming_path='',
            result_template_name='recursivegarden.com/index.html'
        ),
        dict(
            root_host='recursivegarden.com',
            incoming_host='socialmemorycomplex.io',
            incoming_path='',
            result_template_name='socialmemorycomplex.io/index.html'
        ),
        dict(
            root_host='recursivegarden.com',
            incoming_host='socialmemorycomplex.io.recursivegarden.com',
            incoming_path='path/to/',
            result_template_name='socialmemorycomplex.io/path/to/index.html'
        ),
        dict(
            root_host='recursivegarden.com',
            incoming_host='socialmemorycomplex.io.recursivegarden.com',
            incoming_path='',
            result_template_name='socialmemorycomplex.io/index.html'
        ),
    ])
    def test_host_name_parsing(
        self,
        root_host,
        incoming_host,
        incoming_path,
        result_template_name
    ):
        with override_settings(ROOT_HOST=root_host):
            response = self.client.get(reverse('room_view') + incoming_path, HTTP_HOST=incoming_host)
            template_names = [
                template.name
                for template in response.templates
            ]
            self.assertIn(result_template_name, template_names)
