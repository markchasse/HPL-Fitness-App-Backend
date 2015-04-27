from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# import from project
from accounts.models import AppCoach, AppStudent
from FitnessApp.utils import file_upload_to


class ExerciseType(models.Model):
    type_name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    type_description = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.type_name


class WorkoutDefinition(models.Model):
    image = models.ImageField(upload_to=file_upload_to, blank=True, null=True, default="default/default_image.png")
    caption = models.CharField(verbose_name=_('Image Caption'), null=True, blank=True, max_length=250)
    introduction_header = models.CharField(verbose_name=_('Introduction Header'), null=False, blank=False,
                                           max_length=500)
    introduction_textfield = models.TextField(verbose_name=_('Introduction Text'))

    warmup_header = models.CharField(verbose_name=_('WarmUp Header'), null=True, blank=True, max_length=500)
    warmup_content = models.CharField(verbose_name=_('WarmUp content'), null=True, blank=True, max_length=800)
    warmup_notes = models.TextField(verbose_name=_('WarmUp Notes'), null=True, blank=True)

    substitution_header = models.CharField(verbose_name=_('Substitution Header'), null=True, blank=True,
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

    exercises = models.ManyToManyField('Exercise', related_name='exercise_workout')

    assigned_to = models.ManyToManyField(AppStudent, through='AssignedWorkout', related_name='assigned_workout')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated"]

    def __unicode__(self):
        return self.introduction_header


class Exercise(models.Model):
    exercise_header = models.CharField(verbose_name=_('Exercise Header'), null=False, blank=False, max_length=500)
    exercise_content = models.CharField(verbose_name=_('Exercise content'), null=True, blank=True, max_length=800)
    exercise_notes = models.TextField(verbose_name=_('Exercise Notes'))
    exercise_type = models.ForeignKey(ExerciseType, related_name='type_of_exercise', null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated"]
    
    def created_get(self,obj):
        now = obj.created
        date_var = datetime.date(now)
        return date_var

    def __unicode__(self):
        return self.exercise_header


class AssignedWorkout(models.Model):
    student = models.ForeignKey(AppStudent, related_name='student_assigned_workout', null=False)
    workout = models.ForeignKey(WorkoutDefinition, related_name='assigned_workouts', null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated"]
        unique_together = ('student', 'workout')

    def __unicode__(self):
        return self.workout.introduction_header


class AssignedWorkoutDate(models.Model):
    assigned_workout = models.ForeignKey(AssignedWorkout, related_name='assigned_dates', null=False, blank=False)
    assigned_date = models.DateTimeField(verbose_name=_('Date to deliver workout'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["assigned_date"]

    def __unicode__(self):
        return self.assigned_date.strftime('%Y-%m-%d')


class ExerciseResult(models.Model):
    note = models.CharField(verbose_name=_('Exercise Note'), null=True, blank=True, max_length=1000)
    time_taken = models.PositiveIntegerField(verbose_name=_('Exercise Time In Seconds'), null=True, blank=True)
    rounds = models.PositiveSmallIntegerField(verbose_name=_('Exercise Rounds'), null=True, blank=True, max_length=10)
    exercise = models.ForeignKey(Exercise, related_name="exercise_result", blank=False, null=False)
    exercise_result_workout_date = models.ForeignKey(AssignedWorkoutDate, related_name="workout_exercise_result",
                                                     blank=False, null=False)
    result_submit_date = models.DateField(verbose_name='Result Submitted Date', null=False, blank=False,
                                          default=timezone.now().date())

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["exercise_result_workout_date"]

    def __unicode__(self):
        return self.exercise.exercise_header


class PersonalBest(models.Model):
    student = models.ForeignKey(AppStudent, related_name='student_personal_best', null=False)
    workout_assigned_date = models.ForeignKey(AssignedWorkoutDate, related_name="assigned_date_personal_best",
                                              blank=False, null=False, unique=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated"]

    def __unicode__(self):
        return self.workout_assigned_date.assigned_date.strftime('%Y-%m-%d')

