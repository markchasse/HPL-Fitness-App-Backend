from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


from utils import file_upload_to
User = 0
Coach = 1
Admin = 2
class AuthUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser,
                     user_role=User, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(
                _('Email is required to create user'))
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser, user_role=user_role, last_login=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, user_role=User, **extra_fields):
        return self._create_user(email, password, False, False, False, user_role=user_role, **extra_fields)

    def create_superuser(self, email, password, user_role=Admin, **extra_fields):
        return self._create_user(email, password, is_staff=True, is_superuser=True, user_role=user_role, **extra_fields)


class AppUser(AbstractBaseUser, PermissionsMixin):
    User = 0
    Coach = 1
    Admin = 2

    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=50)
    email = models.EmailField(verbose_name=_("Email"), unique=True, max_length=255)
    is_staff = models.BooleanField(verbose_name=_('staff'), default=False, null=False)
    is_active = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to=file_upload_to, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USER_ROLES = (
        (User, _('user')),
        (Coach, _('coach')),
        (Admin, _('admin'))
    )

    user_role = models.PositiveSmallIntegerField(verbose_name=_("User Role"), choices=USER_ROLES, default=User,
                                                 blank=False, null=False, max_length=10)
    objects = AuthUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Fitness Application User'
        verbose_name_plural = 'Fitness Application Users'

    def get_full_name(self):
        return ("%s %s" % (self.first_name, self.last_name))

    def get_short_name(self):
        return self.first_name


class AppStudent(models.Model):
    app_user = models.OneToOneField(AppUser, related_name='student_user',primary_key=True)
    parse_installation_id = models.CharField(max_length=100, null=True, blank=True)
    apple_subscription_id = models.CharField(max_length=100, null=True, blank=True)

    Free = 1
    Paid = 2
    SUB_CHOICES = (
        (Free, _('free')),
        (Paid, _('paid')),
    )
    subscription_choices = models.PositiveSmallIntegerField(verbose_name=_("Subscription Choices"),
                                                            choices=SUB_CHOICES,
                                                            default=Free, blank=False, null=False, max_length=10)

    created = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated = models.DateTimeField(auto_now=True,default=timezone.now())

    def __unicode__(self):
        return self.app_user.first_name

    def get_full_name(self):
        return ("%s %s" % (self.app_user.first_name, self.app_user.last_name))


class AppCoach(models.Model):
    app_user = models.OneToOneField(AppUser, related_name='coach_user',primary_key=True)

    created = models.DateTimeField(auto_now_add=True,default=timezone.now())
    updated = models.DateTimeField(auto_now=True,default=timezone.now())

    def __unicode__(self):
        return self.app_user.first_name

    def get_full_name(self):
        return ("%s %s" % (self.app_user.first_name, self.app_user.last_name))



class FitnessAppStudent(AppUser):
    """
        This model is created because Models can not be registered twice in django admin. This is a workaround for
        that since we just create a proxy model which does not create any columns in database.
    """
    class Meta:
        proxy = True

class FitnessAppCoach(AppUser):
    """
        This model is created because Models can not be registered twice in django admin. This is a workaround for
        that since we just create a proxy model which does not create any columns in database.
    """
    class Meta:
        proxy = True


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(AppUser)
    hash = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class ContactUs(models.Model):
    sender = models.ForeignKey(AppUser, related_name="app_user")
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=500, null=False, blank=False)
    message = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated"]
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __unicode__(self):
        return self.subject