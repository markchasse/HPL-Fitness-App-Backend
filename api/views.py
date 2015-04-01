import datetime
from django.db.models import Q
# from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.serializers import WorkOutSubsSerializer, \
    WorkOutResultSerializer, AssignedWorkOutSerializer
from accounts.models import AssignedWorkOut, WorkOutResult, WorkOutSubscription


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class WorkOutViewSet(viewsets.ModelViewSet):
    serializer_class =  WorkOutResultSerializer
    queryset =  WorkOutResult.objects.all()


class SubscriptionViewSet(viewsets.ModelViewSet):
     serializer_class = WorkOutSubsSerializer
     queryset = WorkOutSubscription.objects.all()


class AssignedWorkOutViewSet(ListAPIView):
    serializer_class = AssignedWorkOutSerializer
    queryset = AssignedWorkOut.objects.all()

    def get_queryset(self):
        queryset = super(AssignedWorkOutViewSet, self).get_queryset()
        get_date = self.kwargs.get('date')
        get_date = datetime.datetime.strptime(get_date, '%Y-%M-%d')
        print get_date
        return queryset.filter(assigned_date__lt=get_date)

        # return queryset.filter(
        #                  Q(assigned_date=datetime.datetime.combine(get_date, datetime.time.min))
        #                  |Q(assigned_date= datetime.datetime.combine(get_date, datetime.time.max))
        #                 )



