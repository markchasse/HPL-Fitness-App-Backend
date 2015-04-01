from django.conf.urls import url, include,patterns
from rest_framework import routers
from api import views
from api.views import  WorkOutViewSet, SubscriptionViewSet, AssignedWorkOutViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'result/', WorkOutViewSet, base_name='result')
router.register(r'subscription', SubscriptionViewSet,  base_name='workout_subscription')
# router.register(r'workout', AssignedWorkOutViewSet,  base_name='assigned_workout')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    # url(r'^api-token-auth','rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^workout/(?P<date>\d{4}-\d{2}-\d{2})/$', views.AssignedWorkOutViewSet.as_view()),

)