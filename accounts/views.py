import json
import logging
import uuid
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# import from app
from accounts.forms import LoginForm
from accounts.models import AppStudent, User, PasswordResetRequest
from accounts.serializers import UserSerializer

# import from project
from FitnessApp.utils import SUCCESS_DICT

logger = logging.getLogger(__name__)
# Create your views here.

User = get_user_model()


class Register(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        user = None
        email = request.DATA.get('email', None)
        if email:
            userlist = list(User.objects.filter(email=email))
            if len(userlist) > 0:
                user = userlist[0]

        if user:
            return Response({'message': 'User with this email already exists:'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.DATA)

        if serializer.is_valid():
            serializer.save()

            if serializer.data['user_role'] == 'user':
                try:
                    # subscription = UserSubscription.objects.create()
                    AppStudent.objects.create(app_user_id=serializer.data['id'])
                except Exception as ex:
                    return Response({'success': False, 'detail': _('Student not created.')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                logger.debug('New subscription created for user %s. %s', serializer.data['email'], serializer.data['id'])

            token, created = Token.objects.get_or_create(user_id=serializer.data['id'])
            if created:
                token.save()
                try:
                    if request.FILES:
                        edited_user =User.objects.get(id=serializer.data['id'])
                        edited_user.profile_image = request.FILES['profile_image']
                        edited_user.save()
                        serializer = UserSerializer(edited_user)
                except Exception as ex:
                    return Response({'success': False,'detail': _('Image not uploaded.')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                logger.debug('New Token created for user %s. %s', serializer.data['email'], token.key)
            return Response({'success':True, 'token': token.key,'user':serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenLogin(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        form = LoginForm(request.DATA)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            login_user = authenticate(username=email, password=password)
            if login_user is not None:
                if login_user.is_active:
                    serializer = UserSerializer(login_user)
                    token, created = Token.objects.get_or_create(user=login_user)
                    logger.debug("login_user object: %s, token: %s", login_user.email, token.key)
                    return Response({'success': True, 'token': token.key, 'user': serializer.data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'success': False, "message":
                        "Your account is not active, Please contact administrator"}, status=status.HTTP_403_FORBIDDEN)
            else:
                logger.info('email %s attempt failed for login', email)
                return Response({'token': None, 'message': 'Invalid email or password', 'success': False},
                                status=status.HTTP_200_OK)
        else:
            payload = {
                'errors': [(k, v[0]) for k, v in form.errors.items()]
            }
            logger.debug('Invalid data. %s', payload)
            return Response(json.dumps(payload), status=status.HTTP_400_BAD_REQUEST)

class AccountInformation(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        login_user = request.user
        if login_user.is_active:
            serializer = UserSerializer(login_user)
            logger.debug("account information object: %s", login_user.email)
            return Response({'success': True, 'user': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'success': False, "message":
                "Your account is not active, Please contact administrator"}, status=status.HTTP_403_FORBIDDEN)

class ChangePassword(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        me = request.user
        data = request.DATA
        old_password = data['old_password']
        new_password = data['new_password']
        if me.check_password(old_password):
            me.set_password(new_password)
            me.save()
            return Response(SUCCESS_DICT,status=status.HTTP_200_OK)
        else:
            return Response({"message": "Your old password does not match our records. Please verify and try again",
                             'success': False}, status=status.HTTP_200_OK)


class ForgetPasswordEmail(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.DATA
        user = None
        email = data.get('email', None)
        if email:
            userlist = list(User.objects.filter(email=email))
            if len(userlist) > 0:
                user = userlist[0]
        if not user:
            return Response({"message": "No user with this email exists in the system",'success': False},
                            status=status.HTTP_200_OK)
        else:
            #check for existing request for current user
            existing_requests = PasswordResetRequest.objects.filter(user=user)
            if existing_requests:
                existing_requests.delete() #if existing request exists delete it
            #generate a new user request here
            reset_request = PasswordResetRequest()
            reset_request.user = user
            reset_request.hash = my_random_string()
            reset_request.save()
            to = user.email
            msg = EmailMultiAlternatives("Password Reset",reset_request.hash, settings.DEFAULT_FROM_EMAIL, [to])
            msg.send()
            return Response({"message": "Kindly check your email for code.",'success': True},status=status.HTTP_200_OK)


class ResetPassword(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.DATA
        if not data['password']:
            return Response({"message": "Password Field is required", 'success': False}, status=status.HTTP_200_OK)
        try:
            reset_object = PasswordResetRequest.objects.get(hash=data['reset_code'])
            user = reset_object.user
            user.set_password(data['password'])
            user.save()
            reset_object.delete()
            return Response(SUCCESS_DICT,status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": "Invalid Code", 'success':False}, status=status.HTTP_200_OK)


class DeleteAccount(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = self.request.user
        user.is_active = False
        user.save()
        return Response({"success": True, 'message': "Your account has been deactivated"})


# we putting this function here to resolve circular import with utils present in FitnessApp
def my_random_string(string_length=7):
    """Returns a random string of length string_length."""
    flag = False
    while flag == False:
        random = str(uuid.uuid4()) # Convert UUID format to a Python string.
        random = random.upper() # Make all characters uppercase.
        random = random.replace("-","") # Remove the UUID '-'.
        my_hash = random[0:string_length]
        duplicate_check = PasswordResetRequest.objects.filter(hash=my_hash)
        if not duplicate_check:
            return my_hash
            break;        #although code will never reach here :)



class ParseInstallation(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.DATA
        if not data['parse_installation_id']:
            return Response({"message": "Parse installation id is required", 'success': False}, status=status.HTTP_200_OK)
        try:
            user = self.request.user
            student = AppStudent.objects.get(app_user=user)
            student.parse_installation_id = data['parse_installation_id']
            student.save()
            return Response(SUCCESS_DICT,status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": "Error saving parse installation id", 'success':False}, status=status.HTTP_200_OK)


    def get(self, request):
        login_user = request.user
        if login_user.is_active:
            try:
                student = AppStudent.objects.get(app_user=login_user)
                logger.debug("Parse installation id: %s", login_user.email)
                return Response({'success': True, 'parse_installation_id': student.parse_installation_id},
                                status=status.HTTP_200_OK) if student.parse_installation_id else Response({'success': False,
                               'message': 'You don not have parse subscription.'},status=status.HTTP_200_OK)
            except Exception as ex:
                return Response({"message": "Error getting parse installation id", 'success':False}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, "message":
                "Your account is not active, Please contact administrator"}, status=status.HTTP_403_FORBIDDEN)


class AppleSubscription(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.DATA
        if not data['apple_subscription_id']:
            return Response({"message": "Apple subscription id is required", 'success': False}, status=status.HTTP_200_OK)
        try:
            user = self.request.user
            student = AppStudent.objects.get(app_user=user)
            student.apple_subscription_id = data['apple_subscription_id']
            student.subscription_choices = 2
            student.save()
            return Response(SUCCESS_DICT,status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": "Error saving Apple subscription id", 'success':False}, status=status.HTTP_200_OK)

    def get(self, request):
        login_user = request.user
        if login_user.is_active:
            try:
                student = AppStudent.objects.get(app_user=login_user)
                logger.debug("Apple subscription id: %s", login_user.email)
                return Response({'success': True, 'apple_subscription_id': student.apple_subscription_id},
                                status=status.HTTP_200_OK) if student.apple_subscription_id else Response({'success': False,
                               'message': 'You don not have Apple subscription.'},status=status.HTTP_200_OK)
            except Exception as ex:
                return Response({"message": "Error getting Apple subscription id", 'success':False}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, "message":
                "Your account is not active, Please contact administrator"}, status=status.HTTP_403_FORBIDDEN)
