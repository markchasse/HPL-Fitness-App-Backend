__author__ = 'apple'
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email="admin@hplfitnessapp.com").exists():
            User.objects.create_superuser("admin@hplfitnessapp.com", "admin")