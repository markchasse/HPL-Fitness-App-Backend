from django import forms
from django.contrib.auth import get_user_model
from accounts.models import AppUser
User = get_user_model()

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = (
            'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):

        super(UserCreationForm, self).__init__(*args, **kwargs)