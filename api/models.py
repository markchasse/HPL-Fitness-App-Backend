import binascii
import os
from django.contrib.admin import exceptions
from django.contrib.auth import authenticate
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from accounts.models import AppUser

#
# @python_2_unicode_compatible
# class Token(models.Model):
#     key = models.CharField(max_length=40, primary_key=True)
#     user = models.OneToOneField(AppUser, related_name='auth_token')
#     created = models.DateTimeField(auto_now_add=True)
#
#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         return super(Token, self).save(*args, **kwargs)
#
#     def generate_key(self):
#         return binascii.hexlify(os.urandom(20)).decode()
#
#     def __str__(self):
#         return self.key
#
#
# class TokenAuthenticate(TokenAuthentication):
#     def __init__(self):
#         super(TokenAuthenticate, self).__init__()
#     model = Token
#
#     def authenticate_credentials(self, key):
#         try:
#             token = self.model.objects.get(key=key)
#         except self.model.DoesNotExist:
#             raise exceptions.AuthenticationFailed('invalid token')
#
# class BasicAuthenticate(BasicAuthentication):
#     def __init__(self):
#         super(BasicAuthenticate, self).__init__()
#
#     def authenticate_credentials(self, userid, password):
#
#         user = authenticate(username=userid, password=password)
#         if user is None:
#             raise exceptions.AuthenticationFailed('Invalid username/password')
#             return None
#         return (user, None)

