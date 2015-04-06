import datetime
from django.db.models import Q
# from datetime import datetime
from rest_framework import viewsets, generics
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.serializers import AssignedWorkOutSerializer, SubscriptionSerializers, \
    DefinedWorkOutSerializers, WorkOutResultSerializer
from accounts.models import AssignedWorkOut, WorkOutSubscription, WorkOutResult


#logged in user can check his/her subscription
class SubscriptionViewSet(viewsets.ModelViewSet):
     serializer_class = SubscriptionSerializers
     queryset = WorkOutSubscription.objects.all()

     def get_queryset(self):
        queryset = super(SubscriptionViewSet, self).get_queryset()
        logged_in_user = self.request.user
        return queryset.filter(subscription_id=logged_in_user.student_user.id)


#student can get his/her workout details on a date input by the him/her
class AssignedWorkOutViewSet(ListAPIView):
    serializer_class = AssignedWorkOutSerializer
    queryset = AssignedWorkOut.objects.all()

    def get_queryset(self):
        queryset = super(AssignedWorkOutViewSet, self).get_queryset()
        workout_date = self.kwargs.get('date')
        logged_user = self.request.user
        if logged_user:
            workout_date = datetime.datetime.strptime(workout_date, '%Y-%m-%d')
            query_obj = queryset.filter(student_assigned_workout__id =logged_user.student_user.id,
                                      assigned_date__year=workout_date.year,
                                      assigned_date__month=workout_date.month,
                               assigned_date__day=workout_date.day,)

        return query_obj


#Coach Schedule his/her workout to deliver for a particular day
class ScheduleWorkOut(ListAPIView):
    serializer_class = DefinedWorkOutSerializers


class ResultViewSet(viewsets.ModelViewSet):
    serializer_class =  WorkOutResultSerializer
    queryset =  WorkOutResult.objects.all()

    def get_queryset(self):
         queryset = super(ResultViewSet, self).get_queryset()
         logged_user = self.request.user
         if logged_user:

             query_obj = queryset.filter( student_id__id = logged_user.student_user.id)

         return query_obj
