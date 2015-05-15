from django.conf.urls import patterns, url
from accounts.views import Register, TokenLogin,DeleteAccount,ChangePassword,ForgetPasswordEmail, ResetPassword, AccountInformation

urlpatterns = patterns('',
    url(r'^register/$', Register.as_view(), name='register_user'),
    url(r'^login/$', TokenLogin.as_view(), name='token_login'),
    url(r'^account_information$', AccountInformation.as_view(), name='account_information'),
    url(r'^password/change/$', ChangePassword.as_view(), name='change-password'),
    url(r'^forget_password/$', ForgetPasswordEmail.as_view()),
    url(r'^reset_password/$', ResetPassword.as_view()),
    url(r'^delete_account/$', DeleteAccount.as_view()),

)
