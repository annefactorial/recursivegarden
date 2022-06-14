from django.views import generic
from django.conf import settings
from django.urls import reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from rest_framework import serializers
from rest_framework import generics, mixins, views
from rest_framework import viewsets


'''
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'uuid',
            'timestamp',
        ]



class EventViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
'''


class GETToFormInitialMixin:
    def get_initial(self):
        initial = super().get_initial()
        for key, value in list(self.request.GET.items()):
            initial[key] = value
        return initial


class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)


class DonationPageView(generic.TemplateView):
    template_name = 'core/donation.html'


class DomainView(generic.TemplateView):
    def get_template_names(self):
        http_host = self.request.META.get('HTTP_HOST')
        root_host = settings.ROOT_HOST

        #TODO use ALLOWED_HOSTS as a whitelist
        if http_host.startswith(root_host):
            domain_name = root_host
        elif root_host in http_host:
            domain_name = http_host.split(f'.{root_host}')[0]
        else:
            domain_name = http_host

        return [
            domain_name.replace('/', '.') + '.html',
            'base.html',
        ]
