import datetime
from datetime import date
from django.http.response import HttpResponse

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from api.serializers import AssignedWorkoutSerializer, SubscriptionSerializers, \
    DefinedWorkoutSerializers, WorkoutResultSerializer, GetResultSerializer, UpdateWorkoutSerializer
from accounts.models import UserSubscription, AppStudent
from workouts.models import AssignedWorkout, WorkoutResult


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
    serializer_class = AssignedWorkoutSerializer
    queryset = AssignedWorkout.objects.all()

    def get_queryset(self):
        queryset = super(AssignedWorkoutViewSet, self).get_queryset()
        result = []
        if self.request.GET.get('date'):
            workout_date = self.request.GET.get('date')
            logged_user = self.request.user
            if logged_user:
                workout_date = datetime.datetime.strptime(workout_date, '%Y-%m-%d')
                query_obj = queryset.filter(assigned_date__lte=workout_date,
                                            student__id=logged_user.student_user.id,
                                           )
                for workout in query_obj:
                    if WorkoutResult.objects.filter(assigned_workout=workout).count() <= 0:
                        result.append(workout)

        return result


#Coach Schedule his/her workout to deliver for a particular day
class ScheduleWorkout(ListAPIView):
    serializer_class = DefinedWorkoutSerializers


class ResultViewSet(viewsets.ViewSet):
    serializer_class = WorkoutResultSerializer
    queryset = WorkoutResult.objects.all()

    def create(self, request, **kwargs):
        logged_in_user = self.request.user.student_user.id
        if request.method == 'POST':
            data = request.DATA.copy()
            serializer = WorkoutResultSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data, 'success': True}, status=status.HTTP_201_CREATED)
            return Response({'success': False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, **kwargs):
       try:
        queryset = WorkoutResult.objects.all()
        result_id = self.kwargs.get('id')
        query_obj = queryset.get(id=result_id)
        serializer = WorkoutResultSerializer(query_obj)
        return Response(serializer.data)
       except Exception as e:
        return Response({'success': False, 'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, *args, **kwargs):
        try:
            serializer = UpdateWorkoutSerializer(data=self.request.DATA)
            if serializer.is_valid():
                workout_result = WorkoutResult.objects.get(pk=self.request.DATA.get('id'))
                serializer = UpdateWorkoutSerializer(workout_result, data=self.request.DATA, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            else:
                return Response({'success': False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
