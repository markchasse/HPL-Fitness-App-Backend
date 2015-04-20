import datetime

from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework import mixins

from api.serializers import AssignedWorkoutSerializer, SubscriptionSerializers, \
    DefinedWorkoutSerializer, ExerciseResultSerializer, GetResultSerializer, UpdateWorkoutSerializer
from accounts.models import UserSubscription, AppStudent
from workouts.models import WorkoutDefinition, AssignedWorkout, AssignedWorkoutDate, Exercise, ExerciseResult


#logged in user can check his/her subscription
class SubscriptionViewSet(viewsets.ViewSet):
    serializer_class = SubscriptionSerializers

    def get(self, request, pk=None, **kwargs):
        queryset = UserSubscription.objects.all()
        logged_in_user = self.request.user
        query_obj = queryset.get(subscription_id=logged_in_user.student_user.id)
        serializer = SubscriptionSerializers(query_obj)
        return Response(serializer.data)


#student can get his/her workout details on a date input by the him/her
class AssignedWorkoutViewSet(ListAPIView):
    serializer_class = DefinedWorkoutSerializer
    queryset = WorkoutDefinition.objects.all()

    def get_queryset(self):
        logged_in_user = self.request.user
        queryset = super(AssignedWorkoutViewSet, self).get_queryset()
        workout_date = self.request.QUERY_PARAMS.get('workout_date', None)
        if workout_date:
            workout_date = datetime.datetime.strptime(workout_date, '%Y-%m-%d')
            queryset = queryset.filter(assigned_workouts__assigned_dates__assigned_date__year=workout_date.year,
                                       assigned_workouts__assigned_dates__assigned_date__month=workout_date.month,
                                       assigned_workouts__assigned_dates__assigned_date__day=workout_date.day,
                                       assigned_workouts__student=logged_in_user.student_user)
            return queryset
        return []


#Coach Schedule his/her workout to deliver for a particular day
class ScheduleWorkout(ListAPIView):
    serializer_class = DefinedWorkoutSerializer


class ResultViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = ExerciseResultSerializer
    queryset = ExerciseResult.objects.all()
    parser_classes = (JSONParser,)

    def get_queryset(self):
        logged_in_student = self.request.user.student_user
        exercise_result_id = self.request.QUERY_PARAMS.get('id', None)
        queryset = super(ResultViewSet, self).get_queryset()
        if exercise_result_id:
            return queryset.filter(id=exercise_result_id, exercise_result_workout__student=logged_in_student)
        return []

    def create(self, request, **kwargs):
        logged_in_student = self.request.user.student_user
        exercise_result_objects = request.data
        serializer_list = []

        for exercise_result_key in exercise_result_objects:
            data = exercise_result_objects[exercise_result_key]
            if 'exercise' in data:
                try:
                    exercise = Exercise.objects.get(id=data['exercise'])
                except Exercise.DoesNotExist:
                    pass
            if 'workout' in data:
                try:
                    workout = WorkoutDefinition.objects.get(id=data['workout'])
                except WorkoutDefinition.DoesNotExist:
                    return Response({'success': False, 'detail': 'Invalid Workout id.', 'object': exercise_result_key},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'success': False, 'detail': '"workout" is a required parameter.',
                                 'object': exercise_result_key}, status=status.HTTP_404_NOT_FOUND)
            assigned_workout = AssignedWorkout.objects.filter(student=logged_in_student, workout=workout)
            if not assigned_workout:
                return Response({'success': False, 'detail': 'Invalid Workout id.', 'object': exercise_result_key},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                data['exercise_result_workout'] = assigned_workout[0].id
            serializer = ExerciseResultSerializer(data=data)
            if not serializer.is_valid():
                return Response({'success': False, 'detail': serializer.errors, 'object': exercise_result_key},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer_list.append(serializer)

        with transaction.atomic():
            for serializer in serializer_list:
                serializer.save()
            return Response({'success': True, 'detail': 'All exercises saved successfully'},
                            status=status.HTTP_201_CREATED)

        return Response({'success': False, 'detail': "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        self.kwargs['pk'] = request.QUERY_PARAMS.get('id', None)
        data = request.DATA.copy()
        if 'exercise_result_workout' in data:
            del data['exercise_result_workout']
        instance = self.get_object()
        data['exercise'] = instance.exercise.id
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     try:
    #         serializer = ExerciseResultSerializer(data=self.request.DATA)
    #         if serializer.is_valid():
    #             workout_result = ExerciseResult.objects.get(pk=self.request.DATA.get('id'))
    #             serializer = UpdateWorkoutSerializer(workout_result, data=self.request.DATA, partial=True)
    #             if serializer.is_valid():
    #                 serializer.save()
    #                 return Response(serializer.data)
    #         else:
    #             return Response({'success': False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'success': False, 'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
