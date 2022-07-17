from django.http import Http404
from django.conf import settings
from django.urls import reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import serializers
from rest_framework import generics, mixins, views
from rest_framework import viewsets

from core.models import Card


class GETToFormInitialMixin:
    def get_initial(self):
        initial = super().get_initial()
        for key, value in list(self.request.GET.items()):
            initial[key] = value
        return initial


class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)


'''
If you go to a slug url (including the bare domain, slug == '/'):
    search for a card with that slug
        if it exists, render that page
        if it doesn't exist
            if you are logged in and have permission, show a create new card form
            if you are not logged in, show a 404
If you go to a uuid url:
    search for a card with that uuid
        if it exists, render that page
        if it doesn't exist, 404

Cards are recursive in nature, you can edit the subpages as well
'''


def card_by_uuid(request, uuid):
    try:
        card = Card.objects.get(uuid=uuid, site=request.site)
    except Card.DoesNotExist:
        raise Http404

    return render_card(request, card)


def card_by_url(request, url=''):
    if not url.endswith('/'):
        url += '/'
    try:
        card = Card.objects.get(url=url, site=request.site)
    except Card.DoesNotExist:
        raise Http404

    return render_card(request, card)


def render_card(request, card):
    if not card.published and not request.user.is_authenticated:
        raise Http404

    return render(request, 'core/card.html', {
        'site': request.site,
        'card': card,
    })
    '''
    match request.headers.get('content-type', 'text/html'):
        case 'text/html':
            pass

        case 'application/json':
            return serialize(card)

        case _:
            raise Http404
    '''
