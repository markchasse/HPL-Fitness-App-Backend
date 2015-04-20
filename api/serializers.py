import json
from datetime import datetime
from datetime import time
from django.core import serializers as django_serializer
from requests.api import request
from rest_framework import serializers
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

from accounts.models import AppUser, AppStudent, UserSubscription, AppCoach
from workouts.models import ExerciseResult, ExerciseType, AssignedWorkout, WorkoutDefinition, Exercise
from workouts import EXERCISE_TYPE_TIME, EXERCISE_TYPE_ROUNDS


class WorkTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseType
        exclude = ('created', 'updated',)


class ExerciseSerializers(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        exclude = ('created', 'updated')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = ('first_name', 'last_name','email')


class CoachSerializer(serializers.ModelSerializer):
    app_user = UserSerializer(read_only=True)

    class Meta:
        model = AppCoach
        fields = ('app_user',)


class DefinedWorkoutSerializer(serializers.ModelSerializer):
    exercises = serializers.SerializerMethodField()
    coach = CoachSerializer(read_only=True)
    next_workout = serializers.SerializerMethodField()
    prev_workout = serializers.SerializerMethodField()

    def get_next_workout(self, obj):
        workout_date = self.context['request'].QUERY_PARAMS.get('workout_date', None)
        workout_date = datetime.strptime(workout_date, '%Y-%m-%d')
        logged_in_user = self.context['request'].user
        assigned_workout = AssignedWorkout.objects.filter(assigned_dates__assigned_date__gt=datetime.combine(
            workout_date, time.max), student_id=logged_in_user.student_user.id).order_by('assigned_dates__assigned_date')
        if assigned_workout:
            next_workout_datetime = assigned_workout[0].assigned_dates.all().filter(assigned_date__gt=datetime.combine(
                                    workout_date, time.max)).order_by('assigned_date')
            if next_workout_datetime:
                return next_workout_datetime[0].assigned_date.date()
        return ""

    def get_prev_workout(self, obj):
        workout_date = self.context['request'].QUERY_PARAMS.get('workout_date', None)
        workout_date = datetime.strptime(workout_date, '%Y-%m-%d')
        logged_in_user = self.context['request'].user
        assigned_workout = AssignedWorkout.objects.filter(assigned_dates__assigned_date__lt=datetime.combine(
            workout_date, time.min), student_id=logged_in_user.student_user.id).order_by('-assigned_dates__assigned_date')
        if assigned_workout:
            prev_workout_datetime = assigned_workout[0].assigned_dates.all().filter(assigned_date__lt=datetime.combine(
                                    workout_date, time.min)).order_by('-assigned_date')
            if prev_workout_datetime:
                return prev_workout_datetime[0].assigned_date.date()
        return ""

    def get_exercises(self, obj):
        if obj:
            exercises = []
            for exercise in obj.exercises.all():
                exercise_dict = {'id': exercise.id}
                exercise_dict['exercise_header'] = exercise.exercise_header
                exercise_dict['exercise_content'] = exercise.exercise_content
                exercise_dict['exercise_notes'] = exercise.exercise_notes
                exercise_dict['exercise_type'] = exercise.exercise_type.type_name

                exercises.append(exercise_dict)

            return exercises
        return []

    class Meta:
        model = WorkoutDefinition
        exclude = ('created', 'updated', 'assigned_to')


class AssignedWorkoutSerializer(serializers.ModelSerializer):
    workout = DefinedWorkoutSerializer(read_only=True)
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


class StudentSerializer(serializers.ModelSerializer):
    app_user = UserSerializer(read_only=True)

    class Meta:
        model = AppStudent
        fields = ('app_user',)


class AssignedWorkoutResult(serializers.ModelSerializer):
    workout = DefinedWorkoutSerializer(read_only=True)

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


class ExerciseResultSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = ExerciseResult
        fields = ('id', 'time_taken', 'rounds', 'note', 'exercise', 'exercise_result_workout')
        read_only_fields = ('id',)
        write_only_fields = ('exercise_result_workout',)

    def validate(self, data):
        """
        Check that the Exercise exists and if it's type is Round than the data contains 'rounds' parameter and if and
        if it's type is Time than it has the time_taken parameter.
        """
        exercise = data['exercise']
        if exercise.exercise_type.type_name == EXERCISE_TYPE_TIME:
            if 'rounds' in data:
                del data['rounds']
            if 'time_taken' not in data:
                raise serializers.ValidationError("time_taken parameter is required for this exercise.")
        elif exercise.exercise_type.type_name == EXERCISE_TYPE_ROUNDS:
            if 'time_taken' in data:
                del data['time_taken']
            if 'rounds' not in data:
                raise serializers.ValidationError("rounds parameter is required for this exercise.")

        return data


class UpdateWorkoutSerializer(ExerciseResultSerializer):
    id = serializers.IntegerField(source='pk')


class GetResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk')

    class Meta:
        model = ExerciseResult
        fields = ('id', 'time', 'assigned_workout', 'rounds', 'note')
