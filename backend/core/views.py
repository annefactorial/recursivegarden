from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateUserForm
from .models import User, Card


class GETToFormInitialMixin:
    def get_initial(self):
        initial = super().get_initial()
        for key, value in list(self.request.GET.items()):
            initial[key] = value
        return initial


class UserCreateView(
        GETToFormInitialMixin,
        generic.CreateView):
    model = User
    template_name = 'core/user_form.html'
    form_class = CreateUserForm

    def get_success_url(self):
        return reverse('user_list')


class UserCreateComponent(generic.CreateView):
    model = User
    template_name = 'core/user_form.html'
    form_class = CreateUserForm


'''
class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)
'''


class CardDetailComponent(generic.DetailView):
    '''
    Autocomplete widget to search for existing components
    '''
    model = Card


class CardListComponent(generic.ListView):
    model = Card


class CardAutocompleteComponent(generic.ListView):
    model = Card


class RoomView(generic.TemplateView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        self.kwargs.path
        pass


class PrivateRoomView(
        LoginRequiredMixin,
        generic.TemplateView):
    pass


class DonationPageView(
        generic.TemplateView):
    template_name = 'core/donation.html'

