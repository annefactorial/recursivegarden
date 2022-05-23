from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("login/", TemplateView.as_view(template_name='core/login.html'), name="login"),
    path("components/login-form/", auth_views.LoginView.as_view(template_name='core/components/login_form.html'), name="login_form_component"),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),


    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('components/create/', views.UserCreateComponent.as_view(), name='user_create_component'),


    path("donation/", views.DonationPageView.as_view(), name="donation_page"),

    path("c/<path:path>/", views.RoomView.as_view(), name="room"),

]
