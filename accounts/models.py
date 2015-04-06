import uuid

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
        """
        user = self.model(email=email, user_role=user_role, is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        """

        user = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser, user_role=user_role, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, user_role=User, **extra_fields):
        return self._create_user(email, password, False, False, False, user_role=user_role, **extra_fields)

    def create_superuser(self, email, password, user_role=Admin, **extra_fields):
        return self._create_user(email, password, is_staff=True, is_superuser=True, user_role=user_role, **extra_fields)


class AppUser(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    email = models.EmailField(verbose_name=_("Email"), unique=True,max_length=255)
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

    def get_full_name(self):
        name = '%s %s %s' % self.first_name, self.last_name
        return name

    def get_short_name(self):
        return self.first_name


class AppStudent(models.Model):
    app_user = models.OneToOneField(AppUser,related_name='student_user')

    subscription_id = models.ForeignKey('WorkOutSubscription', related_name='subscription_id')


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.app_user.first_name)


class AppCoach(models.Model):
    app_user = models.OneToOneField(AppUser, related_name='coach_user')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.app_user.first_name)

class PasswordResetRequest(models.Model):
    user = models.ForeignKey(AppUser)
    hash = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class AppStudent(models.Model):
    app_user = models.OneToOneField(AppUser,  related_name='student_user')

    subscription_id = models.ForeignKey('WorkOutSubscription', related_name='subscription_id')


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.app_user.first_name)


# we putting this function here to resolve circular import with utils
def my_random_string(string_length=7):
    """Returns a random string of length string_length."""
    flag = False
    while flag == False:
        random = str(uuid.uuid4()) # Convert UUID format to a Python string.
        random = random.upper() # Make all characters uppercase.
        random = random.replace("-","") # Remove the UUID '-'.
        my_hash = random[0:string_length]
        duplicate_check = PasswordResetRequest.objects.filter(hash=my_hash)
        if not duplicate_check:
            return my_hash
            break;        #although code will never reach here :)


#assigned workouts by coach to specific user/student
class AssignedWorkOut(models.Model):
    student_assigned_workout = models.ForeignKey("AppStudent", related_name='student_assigned_workout')
    defined_work_out_id = models.ForeignKey("WorkOutDefinition", related_name='defined_workout_id')

    assigned_date = models.DateTimeField(verbose_name=_('Date to deliver workout'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.defined_work_out_id.defined_work_out_title)


#coach define his workout for students/users
class WorkOutDefinition(models.Model):
    workout_type = models.ForeignKey("WorkOutType")
    defined_work_out_text = models.TextField(verbose_name=_('Defined Work Out Text'), null=False, blank=False, max_length=500)
    defined_work_out_title = models.CharField(verbose_name=_('Defined Work Out title'), null=False, blank=False,
                                              max_length=100)
    workout_image = models.ImageField(upload_to=file_upload_to, blank=True, null=True,
                                      default="default/default_image.png")

    workout_image_caption = models.CharField(verbose_name=_('Workout image caption'),null=True, blank=True, max_length=50)
    coach_defined_workout = models.ForeignKey("AppCoach", related_name='coach_defined_workout', null= False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return str(self.defined_work_out_title)


class WorkOutType(models.Model):

    workout_type = models.CharField(verbose_name=_('Workout Type'), null=False, blank=False, max_length=500)

    def __unicode__(self):
        return str(self.workout_type)


class WorkOutResult(models.Model):
    work_out_note = models.CharField(verbose_name=_('Workout Note'),null=True, blank=True, max_length=200)
    work_out_time = models.TimeField()
    work_out_rounds = models.PositiveSmallIntegerField(verbose_name=_('Workout Rounds'), null=True, max_length=10)
    student_id = models.ForeignKey(AppStudent, related_name="app_student", blank=True, null=True)
    assigned_workout_id = models.ForeignKey(AssignedWorkOut, related_name="app_workout", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class WorkOutSubscription(models.Model):
    Free = 1
    Paid = 2
    SUB_CHOICES = (
        (Free, _('free')),
        (Paid, _('paid')),
    )
    subscription_choices = models.PositiveSmallIntegerField(verbose_name=_("Subscription Choices"),
                                                            choices=SUB_CHOICES,
                                                            default=Free,blank=False, null=False, max_length=10)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
