from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
import logging
from accounts.models import AppUser

User = get_user_model()
logger = logging.getLogger(__name__)

class UserCreationForm(forms.ModelForm):

    MIN_LENGTH = settings.PASSWORD_MIN_LENGTH
    password1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput(render_value=True))
    password2 = forms.CharField(
        label=_('Password confirmation'), widget=forms.PasswordInput(render_value=True))
    user_role = forms.ChoiceField(
        label=_("User Role"), choices=AppUser.USER_ROLES)

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        # At least MIN_LENGTH long
        if len(password) < self.MIN_LENGTH:
            raise forms.ValidationError(
                "The password must be at least %d characters long." % self.MIN_LENGTH)

        # At least one letter and one non-letter
        first_isalpha = password[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password):
            raise forms.ValidationError("The password must contain at least one letter and at least one digit or"
                                        " punctuation character.")
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(
            commit=False)
        try:
            user.set_password(self.cleaned_data["password1"])
            user.save()

        except Exception as e:
            logger.error("Exception occurred while saving User",e)

        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"%s\">this form</a>." % ('password')))
    class Meta:
        model = User
        fields = (
            'email', 'password', 'user_role', 'first_name', 'last_name')

    def clean_password(self):
        return self.initial["password"]

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(
            commit=False)
        return user
