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
    #path('api/', include(router.urls)),
    path('', views.card_by_url, name='card_by_url'),
    path('<uuid:uuid>/', views.card_by_uuid, name='card_by_uuid'),
    path('<url>/', views.card_by_url, name='card_by_url'),
]
