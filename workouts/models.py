from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

# import from project
from accounts.models import AppCoach, AppStudent
from FitnessApp.utils import file_upload_to


class WorkoutType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.name)


class WorkoutDefinition(models.Model):
    image = models.ImageField(upload_to=file_upload_to, blank=True, null=True,
                                      default="default/default_image.png")
    # exercise = models.ForeignKey(Exercise, related_name='exercise', null=False)
    caption = models.CharField(verbose_name=_('image caption'), null=True, blank=True, max_length=250)
    introduction_header = models.CharField(verbose_name=_('Introduction Header'), null=False, blank=False,
                                           max_length=500)
    introduction_textfield = models.TextField(verbose_name=_('Introduction Text'))

    warmup_header = models.CharField(verbose_name=_('WarmUp Header'), null=True, blank=True,
                                           max_length=500)
    warmup_content = models.CharField(verbose_name=_('WarmUp content'), null=True, blank=True, max_length=800)
    warmup_notes = models.TextField(verbose_name=_('WarmUp Notes'), null=True, blank=True)

    substitution_header = models.CharField(verbose_name=_('substitution Header'), null=True, blank=True,
                                           max_length=500)
    substitution_content = models.CharField(verbose_name=_('Substitution content'), null=True, blank=True,
                                            max_length=800)
    substitution_notes = models.TextField(verbose_name=_('Substitution Notes'), null=True, blank=True)

    cooldown_header = models.CharField(verbose_name=_('CoolDown Header'), null=True, blank=True, max_length=500)
    cooldown_content = models.CharField(verbose_name=_('CoolDown content'), null=True, blank=True, max_length=800)
    cooldown_notes = models.TextField(verbose_name=_('CoolDown Notes'), null=True, blank=True)

    extracredit_header = models.CharField(verbose_name=_('Extra credit Header'), null=True, blank=True, max_length=500)
    extracredit_content = models.CharField(verbose_name=_('extra credit content'), null=True, blank=True, max_length=800)
    extracredit_notes = models.TextField(verbose_name=_('Extra Credit Notes'), null=True, blank=True)

    homework_header = models.CharField(verbose_name=_('Home Work Header'), null=True, blank=True, max_length=500)
    homework_content = models.CharField(verbose_name=_('Home Work content'), null=True, blank=True, max_length=800)
    homework_notes = models.TextField(verbose_name=_('Homework Notes'), null=True, blank=True)

    coach = models.ForeignKey(AppCoach, related_name='coach_defined_workout', null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.introduction_header


class Exercise(models.Model):
    workout_header = models.CharField(verbose_name=_('WorkOut Header'), null=False, blank=False,
                                           max_length=500)
    workout_content = models.CharField(verbose_name=_('WorkOut content'), null=True, blank=True, max_length=800)
    workout_notes = models.TextField(verbose_name=_('WorkOut Notes'))
    workout_type = models.OneToOneField(WorkoutType)
    workout = models.ForeignKey(WorkoutDefinition, related_name='exercise_workout', null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def created_get(self,obj):
        now = obj.created
        date_var = datetime.date(now)
        return date_var

    def __unicode__(self):
        return self.workout_header

class AssignedWorkout(models.Model):
    student = models.ForeignKey(AppStudent, related_name='student_assigned_workout', null=False)
    workout = models.ForeignKey(WorkoutDefinition, related_name='defined_workout_id', null=False)

    assigned_date = models.DateTimeField(verbose_name=_('Date to deliver workout'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.workout.introduction_header


class WorkoutResult(models.Model):
    note = models.CharField(verbose_name=_('Workout Note'), null=True, blank=True, max_length=1000)
    time = models.PositiveIntegerField(verbose_name=_('Workout Time'), null=True, blank=True)
    rounds = models.PositiveSmallIntegerField(verbose_name=_('Workout Rounds'), null=True, max_length=10)
    assigned_workout = models.ForeignKey(AssignedWorkout, related_name="app_workout", blank=False, null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
