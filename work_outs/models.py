from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils import file_upload_to
from accounts.models import AppCoach, AppStudent


class WorkOutDefinition(models.Model):
    workout_type = models.ForeignKey("WorkOutType")
    defined_work_out_description = models.TextField(verbose_name=_('Defined Work Out Description'))
    defined_work_out_title = models.CharField(verbose_name=_('Defined Work Out title'), null=False, blank=False,
                                              max_length=100)
    workout_image = models.ImageField(upload_to=file_upload_to, blank=True, null=True,
                                      default="default/default_image.png")

    workout_image_caption = models.CharField(verbose_name=_('Workout image caption'),null=True, blank=True,
                                             max_length=250)
    coach_defined_workout = models.ForeignKey(AppCoach, related_name='coach_defined_workout', null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.defined_work_out_title


class AssignedWorkOut(models.Model):
    student_assigned_workout = models.ForeignKey(AppStudent, related_name='student_assigned_workout', null=False)
    defined_work_out_id = models.ForeignKey(WorkOutDefinition, related_name='defined_workout_id', null=False)

    assigned_date = models.DateTimeField(verbose_name=_('Date to deliver workout'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.defined_work_out_id.defined_work_out_title


class WorkOutType(models.Model):

    work_out_reps = models.PositiveSmallIntegerField(verbose_name=_('Workout Repetitions'), null=True, max_length=10)
    work_out_rounds = models.PositiveSmallIntegerField(verbose_name=_('Workout Rounds'), null=True, max_length=10)

    def __unicode__(self):
        return str(self.workout_type)


class WorkOutResult(models.Model):
    work_out_note = models.CharField(verbose_name=_('Workout Note'),null=True, blank=True, max_length=1000)
    work_out_time = models.PositiveIntegerField(verbose_name=_('Workout Time'), null=True, blank=True)
    work_out_rounds = models.PositiveSmallIntegerField(verbose_name=_('Workout Rounds'), null=True, max_length=10)
    assigned_workout_id = models.ForeignKey(AssignedWorkOut, related_name="app_workout", blank=False, null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


