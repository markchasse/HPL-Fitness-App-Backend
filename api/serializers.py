from datetime import datetime
from datetime import time
from rest_framework import serializers

from accounts.models import AppUser, UserSubscription, AppCoach, ContactUs
from workouts.models import ExerciseResult, AssignedWorkout, WorkoutDefinition, PersonalBest
from workouts import EXERCISE_TYPE_TIME, EXERCISE_TYPE_ROUNDS


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
    current_workout = serializers.SerializerMethodField()
    prev_workout = serializers.SerializerMethodField()

    class Meta:
        model = WorkoutDefinition
        exclude = ('created', 'updated', 'assigned_to')

    def get_next_workout(self, obj):
        workout_date = self.context['request'].QUERY_PARAMS.get('workout_date', None)
        if workout_date:
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

    def get_current_workout(self, obj):
        workout_date = self.context['request'].QUERY_PARAMS.get('workout_date', None)
        if not workout_date:
            workout_date = self.context['request'].QUERY_PARAMS.get('date', None)
        if workout_date:
            workout_date = datetime.strptime(workout_date, '%Y-%m-%d')
            return workout_date.strftime('%Y-%m-%d')
        return ""

    def get_prev_workout(self, obj):
        workout_date = self.context['request'].QUERY_PARAMS.get('workout_date', None)
        if workout_date:
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

    class Meta:
        model = ExerciseResult
        fields = ('id', 'time_taken', 'rounds', 'note', 'exercise', 'exercise_result_workout_date')
        read_only_fields = ('id',)
        write_only_fields = ('exercise_result_workout_date',)

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


class WorkOutResultDateSerializer(serializers.ModelSerializer):

    exercise_result_workout_date = serializers.SerializerMethodField()
    workout = serializers.IntegerField(read_only=True, source="exercise_result_workout_date.assigned_workout.workout.id")

    def get_exercise_result_workout_date(self, obj):
        return obj.exercise_result_workout_date.assigned_date.date().strftime('%Y-%m-%d')

    class Meta:
        model = ExerciseResult
        fields = ('id', 'exercise_result_workout_date', 'workout')
        read_only_fields = ('id', 'exercise_result_workout_date', 'workout')


class WorkOutResultSerializer(serializers.ModelSerializer):
    exercises = serializers.SerializerMethodField()
    coach = CoachSerializer(read_only=True)

    def get_exercises(self, obj):
        if obj:
            exercises = []
            for exercise in obj.exercises.all():
                exercise_dict = {'id': exercise.id}
                exercise_dict['exercise_header'] = exercise.exercise_header
                exercise_dict['exercise_content'] = exercise.exercise_content
                exercise_dict['exercise_notes'] = exercise.exercise_notes
                exercise_dict['exercise_type'] = exercise.exercise_type.type_name

                logged_in_student = self.context['request'].user.student_user
                date_workout_assigned = self.context.get('date_workout_assigned')
                result_queryset = ExerciseResult.objects.filter(exercise_result_workout_date__assigned_workout__student=logged_in_student,
                                                 exercise_result_workout_date__assigned_date__year=date_workout_assigned.year,
                                                 exercise_result_workout_date__assigned_date__month=date_workout_assigned.month,
                                                 exercise_result_workout_date__assigned_date__day=date_workout_assigned.day,
                                                 exercise_result_workout_date__assigned_workout__workout=obj,
                                                 exercise=exercise)

                serializer = ExerciseResultSerializer(result_queryset, read_only=True, many=True)
                exercise_dict['result'] = serializer.data

                exercises.append(exercise_dict)

            return exercises
        return []

    class Meta:
        model = WorkoutDefinition
        exclude = ('created', 'updated', 'assigned_to')


class PersonalBestSerializer(serializers.ModelSerializer):
    workout_id = serializers.SerializerMethodField()
    workout_header = serializers.SerializerMethodField()
    workout_assigned_date_id = serializers.IntegerField(read_only=True, source="workout_assigned_date.id")

    def get_workout_id(self, obj):
        return obj.workout_assigned_date.assigned_workout.workout.id

    def get_workout_header(self, obj):
        return obj.workout_assigned_date.assigned_workout.workout.introduction_header

    class Meta:
        model = PersonalBest
        fields = ('workout_assigned_date_id', 'workout_id', 'workout_header')


class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        fields = ('email', 'subject', 'message', 'sender')
        write_only_fields = ('email', 'subject', 'message', 'sender')