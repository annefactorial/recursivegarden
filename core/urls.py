from django.urls import path, include
from django.views.generic import TemplateView

from . import views
'''
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views


router = DefaultRouter()
router.register('events', views.EventViewSet)
'''


urlpatterns = [
    path('discord/', TemplateView.as_view(template_name='core/discord.html')),
    #path('api/', include(router.urls)),
    path('', views.DomainView.as_view(), name='domain_view'),
]
