from pathlib import Path
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




class RoomView(generic.TemplateView):
    '''
    domain name determines the folder of template,
    path determines which room in that folder,
    possibly an optional view function
    '''

    #def get_context_data(self):
    #    context = super().get_context_data()
    #    context['room'] = room
    #    return context

    def get_template_names(self):
        http_host = self.request.META.get('HTTP_HOST', settings.ROOT_HOST)
        root_host = settings.ROOT_HOST

        # Strip port
        http_host = http_host.split(':')[0]

        # Allow subdomains of non-root domains to point to that domain, for testing
        # socialmemorycomplex.io.localhost -> socialmemorycomplex.io
        # socialmemorycomplex.io.recursivegarden.com -> socialmemorycomplex.io
        #TODO use ALLOWED_HOSTS as a whitelist
        if http_host.endswith(root_host):
            domain_name = http_host.split(f'.{root_host}')[0]
        else:
            domain_name = http_host

        # Choose a template based on the full domain and path
        full_path = domain_name + self.request.path
        if full_path.endswith('/'):
            return [full_path + 'index.html']
        else:
            return [full_path]


