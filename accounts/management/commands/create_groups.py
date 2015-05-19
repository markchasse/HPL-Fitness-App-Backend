__author__ = 'apple'
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Group.objects.filter(name='Free').exists():
            Group.objects.create(name='Free')
        if not Group.objects.filter(name='Paid').exists():
            Group.objects.create(name='Paid')