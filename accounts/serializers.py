

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.ModelField(model_field=User._meta.get_field('email'))
    profilepicture = serializers.SerializerMethodField('get_picture')

    def get_picture(self,obj):
        if obj.profile_image:
            return obj.profile_image.url
        else:
            return None
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password','user_role','profilepicture')
        write_only_fields = ('password',)
#         read_only_fields = ('profilepicture',)

    def create(self, validated_data):
        user = super(UserSerializer,self).create(validated_data)
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user.set_password(validated_data['password'])
        user.save()
        return user
