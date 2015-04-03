from django.conf.urls import url, include,patterns
from rest_framework import routers
from api import views
from api.views import SubscriptionViewSet, ResultViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'subscription', SubscriptionViewSet,  base_name='workout_subscription')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^workout/(?P<date>\d{4}-\d{2}-\d{2})/$', views.AssignedWorkOutViewSet.as_view()),
    url(r'^workout/result/$', views.ResultViewSet.as_view()),

)