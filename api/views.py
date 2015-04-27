import datetime

from django.db import transaction
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework import mixins
from rest_framework.throttling import ScopedRateThrottle

from api.serializers import SubscriptionSerializers, DefinedWorkoutSerializer, ExerciseResultSerializer,\
    WorkOutResultDateSerializer, WorkOutResultSerializer, PersonalBestSerializer, ContactUsSerializer
from FitnessApp.utils import send_custom_email
from workouts import EXERCISE_TYPE_ROUNDS, EXERCISE_TYPE_TIME
from workouts.models import WorkoutDefinition, AssignedWorkoutDate, Exercise, ExerciseResult, \
    PersonalBest


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


def get_value_of_workout_session(exercise_results_of_one_workout_session):
    one_workout_result_sum = 0
    for exercise_result in exercise_results_of_one_workout_session:
        if exercise_result.exercise.exercise_type.type_name == EXERCISE_TYPE_ROUNDS:
            one_workout_result_sum = one_workout_result_sum + exercise_result.rounds
        elif exercise_result.exercise.exercise_type.type_name == EXERCISE_TYPE_TIME:
            one_workout_result_sum = one_workout_result_sum + exercise_result.time_taken

    return one_workout_result_sum


def update_personal_best(student, assigned_workout_date_obj):
    existing_personal_best = PersonalBest.objects.filter(student=student,
                                                         workout_assigned_date__assigned_workout__workout=
                                                         assigned_workout_date_obj.assigned_workout.workout)
    if existing_personal_best:
        existing = ExerciseResult.objects.filter(
            exercise_result_workout_date=existing_personal_best[0].workout_assigned_date)
        to_compare = ExerciseResult.objects.filter(exercise_result_workout_date=assigned_workout_date_obj)

        existing_personal_best_value = get_value_of_workout_session(existing)
        to_compare_personal_best_value = get_value_of_workout_session(to_compare)

        if to_compare_personal_best_value > existing_personal_best_value:
            existing_personal_best[0].workout_assigned_date = assigned_workout_date_obj
            existing_personal_best[0].save()

    else:
        new_personal_best = PersonalBest(student=student, workout_assigned_date=assigned_workout_date_obj)
        new_personal_best.save()


class ResultViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ExerciseResultSerializer
    queryset = ExerciseResult.objects.all()
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get_queryset(self):
        logged_in_student = self.request.user.student_user
        exercise_result_id = self.request.QUERY_PARAMS.get('id', None)
        queryset = super(ResultViewSet, self).get_queryset()
        queryset = queryset.filter(exercise_result_workout_date__assigned_workout__student=logged_in_student)
        if exercise_result_id:
            return queryset.filter(id=exercise_result_id)
        queryset = queryset.order_by('exercise_result_workout_date_id').distinct('exercise_result_workout_date')
        return queryset

    def create(self, request, **kwargs):
        logged_in_student = self.request.user.student_user
        exercise_result_objects = request.data
        serializer_list = []

        workout_assign_date = exercise_result_objects['workout_assign_date']
        workout_assign_date = datetime.datetime.strptime(workout_assign_date, '%Y-%m-%d')
        if not workout_assign_date:
            return Response({'success': False, 'detail': "workout_assign_date is a required parameter."},
                            status=status.HTTP_400_BAD_REQUEST)

        for exercise_result_key in exercise_result_objects:
            if exercise_result_key == 'workout_assign_date':
                continue
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
            assigned_workout_date_id = AssignedWorkoutDate.objects.filter(assigned_workout__student=logged_in_student,
                                                                          assigned_workout__workout=workout,
                                                                          assigned_date__year=workout_assign_date.year,
                                                                          assigned_date__month=workout_assign_date.month,
                                                                          assigned_date__day=workout_assign_date.day)
            if not assigned_workout_date_id:
                return Response({'success': False, 'detail': 'Invalid workout_assign_date .',
                                 'object': exercise_result_key}, status=status.HTTP_400_BAD_REQUEST)
            else:
                data['exercise_result_workout_date'] = assigned_workout_date_id[0].id
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

                update_personal_best(student=logged_in_student, assigned_workout_date_obj=assigned_workout_date_id[0])
                return Response({'success': True, 'detail': 'All exercises saved successfully'},
                                status=status.HTTP_201_CREATED)

        return Response({'success': False, 'detail': "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logged_in_student = self.request.user.student_user
        exercise_result_id = request.QUERY_PARAMS.get('id', None)
        if not exercise_result_id:
            return Response({'success': False, 'detail': 'id is a required parameter.'},
                            status=status.HTTP_400_BAD_REQUEST)
        self.kwargs['pk'] = exercise_result_id
        data = request.DATA.copy()
        if 'exercise_result_workout_date' in data:
            del data['exercise_result_workout_date']
        instance = self.get_object()
        data['exercise'] = instance.exercise.id
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        update_personal_best(logged_in_student, instance.exercise_result_workout_date)

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
    date_workout_assigned = request.QUERY_PARAMS.get('date', None)
    if not workout_id:
        return Response({'success': False, 'detail': 'id is a required parameter.'})
    if not date_workout_assigned:
        return Response({'success': False, 'detail': 'date is a required parameter.'})

    date_workout_assigned = datetime.datetime.strptime(date_workout_assigned, '%Y-%m-%d')
    queryset = WorkoutDefinition.objects.filter(id=workout_id, assigned_workouts__student=logged_in_student)
    if queryset:
        serializer = WorkOutResultSerializer(queryset[0], context={'request': request,
                                                                   'date_workout_assigned': date_workout_assigned})
    else:
        return Response({'success': False, 'detail': 'Invalid Workout id.'})

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def personal_best(request):
    logged_in_student = request.user.student_user
    personal_bests = PersonalBest.objects.filter(student=logged_in_student)

    serializer = PersonalBestSerializer(personal_bests, many=True)
    return Response(serializer.data)


class ContactUsViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'contacts'

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['sender'] = request.user.id
        serializer = ContactUsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            ctx = {
                "to": settings.DEFAULT_TO_EMAIL,
                "from": serializer.instance.email,
                "subject": serializer.instance.subject,
                "message": serializer.instance.message
            }
            send_custom_email(request, ctx)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
