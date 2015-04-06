from rest_framework import serializers

from accounts.models import AppUser,AppStudent, WorkOutSubscription
from work_outs.models import WorkOutResult,WorkOutType,AssignedWorkOut, WorkOutDefinition


class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOutType
        fields = ('id','workout_type',)


class DefinedWorkOutSerializers(serializers.ModelSerializer):
    workout_type = WorkTypeSerializer(read_only=True)

    class Meta:
        model = WorkOutDefinition
        fields = ('workout_type', 'defined_work_out_text', 'defined_work_out_title', 'workout_image_caption', )

class AssignedWorkOutSerializer(serializers.ModelSerializer):
    defined_work_out_id = DefinedWorkOutSerializers(read_only=True)

    class Meta:
        model = AssignedWorkOut
        fields = ('student_assigned_workout', 'defined_work_out_id',)

class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('first_name', 'last_name','email')

class StudentSerializer(serializers.ModelSerializer):
    app_user = LoginSerializers(read_only=True)
    class Meta:
        model = AppStudent
        fields = ('app_user',)

class AssignedWorkOutResult(serializers.ModelSerializer):
    defined_work_out_id = DefinedWorkOutSerializers(read_only=True)

    class Meta:
        model = AssignedWorkOut
        fields = ('defined_work_out_id',)

class SubscriptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = WorkOutSubscription
        fields = ('subscription_choices',)


class WorkOutResultSerializer(serializers.ModelSerializer):
    workout_id = AssignedWorkOutResult(source='assigned_workout_id_id', read_only=True)
    class Meta:
        model = WorkOutResult
        fields =('workout_id','workout_id', 'assigned_workout_id',
                 'work_out_time','work_out_rounds')