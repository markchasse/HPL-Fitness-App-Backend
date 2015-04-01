from django import forms
from django.utils.translation import ugettext_lazy as _

class LoginForm(forms.Form):
    email = forms.EmailField(label=_("Email"), required=True)
    password = forms.CharField(label=_("Password"),widget=forms.PasswordInput(render_value= False), required=True)

class EditProfileForm(forms.Form):
    first_name = forms.CharField(label=_('First Name'), required=False)
    last_name = forms.CharField(label=_('Last Name'), required=False)
    email = forms.EmailField(label=_("Email"), required=False)
    profile_image = forms.ImageField(required=False)