from datetime import datetime
from datetime import time
from rest_framework import serializers

from accounts.models import AppUser, UserSubscription, AppCoach, ContactUs
from workouts.models import WorkoutResult, AssignedWorkout, WorkoutDefinition, PersonalBest, Exercise
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
    workout_type = serializers.SerializerMethodField('workout_choices_get')
    exercises = serializers.SerializerMethodField()
    coach = CoachSerializer(read_only=True)
    is_result_submit = serializers.SerializerMethodField()

    class Meta:
        model = WorkoutDefinition
        exclude = ('created', 'updated', 'assigned_to')

    def get_is_result_submit(self, obj):
        logged_in_student = self.context['request'].user.student_user
        workout_date = self.context['request'].QUERY_PARAMS.get('workout_date', None)
        if workout_date:
            workout_date = datetime.strptime(workout_date, '%Y-%m-%d')
            try:
                result = WorkoutResult.objects.filter(result_workout_assign_date__assigned_workout__workout=obj,
                                                      result_workout_assign_date__assigned_date__year=workout_date.year,
                                                      result_workout_assign_date__assigned_date__month=workout_date.month,
                                                      result_workout_assign_date__assigned_date__day=workout_date.day,
                                                      result_workout_assign_date__assigned_workout__student=logged_in_student
                                                      )
                if result:
                    return True
            except WorkoutResult.DoesNotExist:
                pass
        return False

    def get_exercises(self, obj):
        if obj:
            exercises = []
            for exercise in obj.exercises.all():
                exercise_dict = {}
                exercise_dict['exercise_content'] = exercise.exercise_content
                exercises.append(exercise_dict)

            return exercises
        return []

    def workout_choices_get(self, obj):
         return obj.workout_type.type_name


class WorkoutFormatSerializers(serializers.Serializer):
    next_workout = serializers.SerializerMethodField()
    current_workout = serializers.SerializerMethodField()
    prev_workout = serializers.SerializerMethodField()
    workout = serializers.SerializerMethodField()

    def get_workout(self, obj):
        if obj:
            workout = WorkoutDefinition.objects.filter(id=obj.id)
            serializer = DefinedWorkoutSerializer(workout, many=True,context={'request': self.context['request']})
            return serializer.data
        return []

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

    class Meta:
        model = WorkoutResult
        fields = ('id', 'time_taken', 'rounds','note', 'result_workout_assign_date')
        read_only_fields = ('id',)
        write_only_fields = ('result_workout_assign_date',)

    def validate(self, data):
        """
        Check that the Exercise exists and if it's type is Round than the data contains 'rounds' parameter and if and
        if it's type is Time than it has the time_taken parameter.
        """
        if self.instance:
            workout = self.instance.result_workout_assign_date.assigned_workout.workout
        else:
            workout = data['result_workout_assign_date'].assigned_workout.workout

        if workout.workout_type.type_name == EXERCISE_TYPE_TIME:
            if 'rounds' in data:
                del data['rounds']
            if 'time_taken' not in data:
                raise serializers.ValidationError("time_taken parameter is required for this workout.")
        elif workout.workout_type.type_name == EXERCISE_TYPE_ROUNDS:
            if 'time_taken' in data:
                del data['time_taken']
            if 'rounds' not in data:
                raise serializers.ValidationError("rounds parameter is required for this workout.")

        return data


class WorkOutResultDateSerializer(serializers.ModelSerializer):

    result_workout_assign_date = serializers.SerializerMethodField()
    workout = serializers.IntegerField(read_only=True, source="result_workout_assign_date.assigned_workout.workout.id")

    def get_result_workout_assign_date(self, obj):
        return obj.result_workout_assign_date.assigned_date.date().strftime('%Y-%m-%d')

    class Meta:
        model = WorkoutResult
        fields = ('id', 'result_workout_assign_date', 'workout')
        read_only_fields = ('id', 'result_workout_assign_date', 'workout')

class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        exclude = ('created', 'updated')

class ResultWorkoutDefinitionSerializer(serializers.ModelSerializer):
    workout_type = serializers.SerializerMethodField('workout_choices_get')

    class Meta:
        model = WorkoutDefinition
        fields = ('id', 'workout_type', 'image','caption','workout_nick_name','introduction_header','introduction_textfield','workout_header','workout_content')

    def workout_choices_get(self, obj):
        return obj.workout_type.type_name

class WorkOutResultSerializer(serializers.ModelSerializer):
    # exercises = serializers.SerializerMethodField()
    workout = serializers.SerializerMethodField()
    # exercises = ExerciseSerializer(read_only=True)
    coach = CoachSerializer(read_only=True)

    def get_workout(self, obj):
        if obj:
            # logged_in_student = self.context['request'].user.student_user
            # date_workout_assigned = self.context.get('date_workout_assigned')
            assigned_workout = list(AssignedWorkout.objects.filter(id=obj.result_workout_assign_date_id))[0]
            workout = WorkoutDefinition.objects.filter(id=assigned_workout.workout_id)
            serializer = ResultWorkoutDefinitionSerializer(workout, read_only=True, many=True)

            # exercise_dict['result'] = serializer.data
            return serializer.data
        return []

    def get_exercises(self, obj):
        if obj:
            exercises = []
            for exercise in obj.exercises.all():
                exercise_dict = {}
                exercise_dict['exercise_content'] = exercise.exercise_content
                exercises.append(exercise_dict)

            return exercises
        return []

    class Meta:
        model = WorkoutResult
        exclude = ('created', 'updated')


class PersonalBestSerializer(serializers.ModelSerializer):
    workout_id = serializers.SerializerMethodField()
    workout_header = serializers.SerializerMethodField()
    workout_assigned_date = serializers.SerializerMethodField()

    def get_workout_id(self, obj):
        return obj.workout_assigned_date.assigned_workout.workout.id

    def get_workout_header(self, obj):
        return obj.workout_assigned_date.assigned_workout.workout.introduction_header

    def get_workout_assigned_date(self, obj):
        return obj.workout_assigned_date.assigned_date.strftime('%Y-%m-%d')

    class Meta:
        model = PersonalBest
        fields = ('workout_assigned_date', 'workout_id', 'workout_header')


class LeaderBoardResultSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_avatar = serializers.SerializerMethodField()

    def get_student_name(self,obj):
        return obj.result_workout_assign_date.assigned_workout.student.get_full_name()

    def get_student_avatar(self,obj):
        if obj.result_workout_assign_date.assigned_workout.student.app_user.profile_image:
            return obj.result_workout_assign_date.assigned_workout.student.app_user.profile_image.url
        else:
            return None

    class Meta:
        model = WorkoutResult
        fields = ('student_name', 'student_avatar', 'time_taken', 'rounds','result_submit_date')

class LeaderBoardSerializer(serializers.ModelSerializer):
    leader_board = serializers.SerializerMethodField()
    workout_type = serializers.SerializerMethodField()

    def get_workout_type(self, obj):
        return obj.workout_type.type_name

    def get_leader_board(self, obj):
        workout_date = self.context['request'].QUERY_PARAMS.get('workout_date', None)
        if workout_date:
            workout_date = datetime.strptime(workout_date, '%Y-%m-%d')
            if obj:
                leaders = None
                if obj.workout_type_id == 1:
                    leaders = WorkoutResult.objects.filter(result_workout_assign_date__assigned_workout__workout=obj,
                                                           result_workout_assign_date__assigned_date__year=workout_date.year,
                                                           result_workout_assign_date__assigned_date__month=workout_date.month,
                                                           result_workout_assign_date__assigned_date__day=workout_date.day
                                                            ).order_by('-time_taken')[:5]
                elif obj.workout_type_id == 2:
                    leaders = WorkoutResult.objects.filter(result_workout_assign_date__assigned_workout__workout=obj,
                                                           result_workout_assign_date__assigned_date__year=workout_date.year,
                                                           result_workout_assign_date__assigned_date__month=workout_date.month,
                                                           result_workout_assign_date__assigned_date__day=workout_date.day
                                                        ).order_by('-rounds')[:5]

                serializer = LeaderBoardResultSerializer(leaders, many=True)
                return serializer.data
        return []

    class Meta:
        model = WorkoutDefinition
        fields = ('workout_type', 'image','caption','workout_nick_name','introduction_header','introduction_textfield','workout_header','workout_content','leader_board')

class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        fields = ('email', 'subject', 'message', 'sender')
        write_only_fields = ('email', 'subject', 'message', 'sender')