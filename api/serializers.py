import json
from datetime import datetime
from django.core import serializers as django_serializer
from requests.api import request
from rest_framework import serializers
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

from accounts.models import AppUser, AppStudent, UserSubscription
from workouts.models import WorkoutResult, WorkoutType, AssignedWorkout, WorkoutDefinition, Exercise


class WorkTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutType
        fields = ('id', 'name', 'description',)


class DefinedWorkoutSerializers(serializers.ModelSerializer):

    class Meta:
        model = WorkoutDefinition
        fields = ('introduction_header', 'introduction_textfield', 'warmup_header', 'warmup_content','warmup_notes',
        'substitution_header', 'substitution_content', 'substitution_notes', 'cooldown_header','cooldown_content',
        'cooldown_notes', 'extracredit_header', 'extracredit_content', 'extracredit_notes', 'homework_header',
        'homework_content', 'homework_notes', )



class ExerciseSerializers(serializers.ModelSerializer):
    workout = DefinedWorkoutSerializers(read_only=True)
    workout_type = WorkTypeSerializer(read_only=True)

    class Meta:
        model = Exercise
        fields = ('workout_header', 'workout_content', 'workout_notes', 'workout_type', 'workout')


class AssignedWorkoutSerializer(serializers.ModelSerializer):
    workout = DefinedWorkoutSerializers(read_only=True)
    exercise = serializers.SerializerMethodField('get_workout')

    class Meta:
        model = AssignedWorkout
        fields = ('id', 'student', 'workout', 'exercise')

    def get_workout(self, obj):
        exercise_list = obj.workout.exercise_workout.all()
        data = []
        for exercise in exercise_list:
            data.append({"id": exercise.id, "Excercise":exercise.workout_header,
                         "WorkOut":exercise.workout.introduction_header,
                         "date":exercise.workout.created})
        return data

        return django_serializer.serialize('json', exercise_list)


class LoginSerializers(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = ('first_name', 'last_name','email')


class StudentSerializer(serializers.ModelSerializer):
    app_user = LoginSerializers(read_only=True)

    class Meta:
        model = AppStudent
        fields = ('app_user',)


class AssignedWorkoutResult(serializers.ModelSerializer):
    workout = DefinedWorkoutSerializers(read_only=True)

    class Meta:
        model = AssignedWorkout
        fields = ('workout',)


class SubscriptionSerializers(serializers.ModelSerializer):
    subscription_choices = serializers.SerializerMethodField('subscription_choices_get')
    created = serializers.SerializerMethodField('created_get')
    class Meta:
        model = UserSubscription
        fields = ('subscription_choices','created')

    def subscription_choices_get(self, obj):
         if obj.subscription_choices == 1:
             return "Free"
         else :
             return "Paid"

    def created_get(self,obj):
        now = obj.created
        date_var = datetime.date(now)
        return date_var


class WorkoutResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    exercise = serializers.SerializerMethodField('get_workout')

    class Meta:
        model = WorkoutResult
        fields = ('id', 'assigned_workout', 'time', 'rounds', 'note', 'exercise')

    def get_workout(self, obj):
        exercise_list = obj.assigned_workout.workout.exercise_workout.filter(id=obj.assigned_workout.workout.id)
        data = []
        for exercise in exercise_list:
            data.append({"id": exercise.id, "Excercise":exercise.workout_header,
                         "WorkOut":exercise.workout.introduction_header})

        return data
        # exercise_list_dict = exercise_list.__dict__
        # return json.dumps(list(exercise_list_dict))
        # return django_serializer.serialize('json', exercise_list_dict)


class UpdateWorkoutSerializer(WorkoutResultSerializer):
    id = serializers.IntegerField(source='pk')


class GetResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk')

    class Meta:
        model = WorkoutResult
        fields = ('id', 'time', 'assigned_workout', 'rounds', 'note')
