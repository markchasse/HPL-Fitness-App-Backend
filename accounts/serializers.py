

from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.ModelField(model_field=User._meta.get_field('email'))
    profile_image = serializers.SerializerMethodField('get_picture')
    user_role = serializers.SerializerMethodField()

    def get_picture(self,obj):
        if obj.profile_image:
            return obj.profile_image.url
        else:
            return None

    def get_user_role(self,obj):
        if obj.user_role == 0:
            return 'user'
        elif obj.user_role == 1:
            return 'coach'
        elif obj.user_role == 2:
            return 'Admin'

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password','user_role','profile_image')
        write_only_fields = ('password',)
        read_only_fields = ('id', 'user_role')

    def create(self, validated_data):
        user = super(UserSerializer,self).create(validated_data)
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        try:
            if user.user_role == 0:
                if not Group.objects.filter(name='Free').exists():
                    Group.objects.create(name='Free')
                group = Group.objects.get(name='Free')
                user.groups.add(group)
        except Exception as ex:
            pass
        user.set_password(validated_data['password'])
        user.save()
        return user
