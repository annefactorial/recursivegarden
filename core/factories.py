import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.User'
    email = 'david@recursivegarden.com'
    password = factory.PostGenerationMethodCall('set_password', 'password')
