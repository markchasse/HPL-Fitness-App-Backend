from rest_framework import serializers
from accounts.models import AppUser,AppStudent, WorkOutDefinition, WorkOutResult, WorkOutSubscription, \
    AssignedWorkOut, \
    WorkOutType


class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOutType
        fields = ('workout_type',)


class DefinedWorkOutSerializers(serializers.ModelSerializer):
    workout_type = WorkTypeSerializer(read_only=True)

    class Meta:
        model = WorkOutDefinition
        fields = ('workout_type', 'defined_work_out_text', 'defined_work_out_title', 'workout_image_caption', )

class AssignedWorkOutSerializer(serializers.ModelSerializer):
    defined_work_out_id = DefinedWorkOutSerializers(read_only=True)
    class Meta:
        model = AssignedWorkOut
        fields = ('student_assigned_workout', 'defined_work_out_id',  'assigned_date',)


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('first_name', 'last_name','email')

class StudentSerializer(serializers.ModelSerializer):
    app_user =  LoginSerializers(read_only=True)
    class Meta:
        model = AppStudent
        fields = ('app_user.first_name',)

class SubscriptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = WorkOutSubscription
        fields = ('subscription_choices',)


class WorkOutResultSerializer(serializers.ModelSerializer):
    workout_id = AssignedWorkOutSerializer(many=True, read_only=True)

    class Meta:
        model = WorkOutResult
        fields =('student_id','assigned_workout_id', 'workout_id' ,'work_out_time',
                 'work_out_rounds')