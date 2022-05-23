from django import forms
from .models import User


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', max_length=255, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'display_name',
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        #instance.send_activation_email()
        instance.set_password(self.cleaned_data["password"])
        instance.save(commit)
        return instance

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
