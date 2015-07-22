from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from accounts.views import Register, TokenLogin,DeleteAccount,ChangePassword,ForgetPasswordEmail,\
    ResetPassword, AccountInformation, ParseInstallation, AppleSubscription

urlpatterns = patterns('',
    url(r'^register/$', csrf_exempt(Register.as_view()), name='register_user'),
    url(r'^login/$', csrf_exempt(TokenLogin.as_view()), name='token_login'),
    url(r'^account_information$', AccountInformation.as_view(), name='account_information'),
    url(r'^password/change/$', csrf_exempt(ChangePassword.as_view()), name='change-password'),
    url(r'^forget_password/$', csrf_exempt(ForgetPasswordEmail.as_view())),
    url(r'^reset_password/$', csrf_exempt(ResetPassword.as_view())),
    url(r'^delete_account/$', csrf_exempt(DeleteAccount.as_view())),
    url(r'^parse_installation/$', ParseInstallation.as_view()),
    url(r'^apple_subscription/$', AppleSubscription.as_view()),

)
