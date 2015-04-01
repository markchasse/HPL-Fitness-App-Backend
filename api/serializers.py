from rest_framework import serializers
from accounts.models import AppUser, DefinedWorkOut, WorkOutResult, WorkOutSubscription,AssignedWorkOut
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class WorkOutResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOutResult
        fields =('work_out_time', 'work_out_rounds')


class WorkOutSubsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOutSubscription
        fields =('sub_choices',)


class AssignedWorkOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignedWorkOut
        fields = ('student_assigned_workout', 'defined_work_out_id',  'assigned_date')



class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('first_name', 'last_name','email')