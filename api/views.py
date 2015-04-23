import datetime

from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework import mixins

from api.serializers import SubscriptionSerializers, DefinedWorkoutSerializer, ExerciseResultSerializer,\
    WorkOutResultDateSerializer, WorkOutResultSerializer
from accounts.models import UserSubscription
from workouts.models import WorkoutDefinition, AssignedWorkout, Exercise, ExerciseResult


#logged in user can check his/her subscription
class SubscriptionViewSet(viewsets.ViewSet):
    serializer_class = SubscriptionSerializers

    def get(self, request, pk=None, **kwargs):
        logged_in_student = self.request.user.student_user
        serializer = SubscriptionSerializers(logged_in_student.subscription)
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


class ResultViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ExerciseResultSerializer
    queryset = ExerciseResult.objects.all()
    parser_classes = (JSONParser,)

    def get_queryset(self):
        logged_in_student = self.request.user.student_user
        exercise_result_id = self.request.QUERY_PARAMS.get('id', None)
        queryset = super(ResultViewSet, self).get_queryset()
        queryset = queryset.filter(exercise_result_workout__student=logged_in_student)
        if exercise_result_id:
            return queryset.filter(id=exercise_result_id)
        return queryset.order_by('result_submit_date').distinct('result_submit_date')

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

        if serializer_list:
            with transaction.atomic():
                for serializer in serializer_list:
                    serializer.save()
                return Response({'success': True, 'detail': 'All exercises saved successfully'},
                                status=status.HTTP_201_CREATED)

        return Response({'success': False, 'detail': "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        exercise_result_id = request.QUERY_PARAMS.get('id', None)
        if not exercise_result_id:
            return Response({'success': False, 'detail': 'id is a required parameter.'},
                            status=status.HTTP_400_BAD_REQUEST)
        self.kwargs['pk'] = exercise_result_id
        data = request.DATA.copy()
        if 'exercise_result_workout' in data:
            del data['exercise_result_workout']
        instance = self.get_object()
        data['exercise'] = instance.exercise.id
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = WorkOutResultDateSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = WorkOutResultDateSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def workout_result(request):
    logged_in_student = request.user.student_user
    workout_id = request.QUERY_PARAMS.get('id', None)
    date_result_submitted = request.QUERY_PARAMS.get('date', None)
    if not workout_id:
        return Response({'success': False, 'detail': 'id is a required parameter.'})
    if not date_result_submitted:
        return Response({'success': False, 'detail': 'date is a required parameter.'})

    date_result_submitted = datetime.datetime.strptime(date_result_submitted, '%Y-%m-%d')
    queryset = WorkoutDefinition.objects.filter(id=workout_id, assigned_workouts__student=logged_in_student)
    if queryset:
        serializer = WorkOutResultSerializer(queryset[0], context={'request': request,
                                                                   'date_result_submitted': date_result_submitted})
    else:
        return Response({'success': False, 'detail': 'Invalid Workout id.'})

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def personal_best(request):
    WorkoutDefinition.objects.filter()
    logged_in_student = request.user.student_user
    exercise_result_id = request.QUERY_PARAMS.get('id', None)

    queryset = ExerciseResult.objects.filter(exercise_result_workout__student=logged_in_student)

    return queryset.order_by('result_submit_date').distinct('result_submit_date')

# class WorkOutResult(viewsets.ReadOnlyModelViewSet):
#     serializer_class = WorkOutResultDateSerializer
#     queryset = ExerciseResult.objects.all()
#
#     def get_queryset(self):
#         logged_in_student = self.request.user.student_user
#         queryset = super(WorkOutResult, self).get_queryset()
#         queryset = queryset.filter(exercise_result_workout__student=logged_in_student).\
#             order_by('result_submit_date').distinct('result_submit_date')
#
#         return queryset