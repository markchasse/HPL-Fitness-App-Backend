from django.conf.urls import url, include, patterns
from rest_framework import routers

from api.views import AssignedWorkoutViewSet, SubscriptionViewSet, ResultViewSet


router = routers.DefaultRouter(trailing_slash=False)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^workout/$', AssignedWorkoutViewSet.as_view()),

    url(r'^result/(?P<id>\d+)$', ResultViewSet.as_view({'get': 'get'})),
    url(r'^result/$', ResultViewSet.as_view({'post': 'create', 'put': 'update'})),
    url(r'^subscription/$', SubscriptionViewSet.as_view({'get': 'get'})),

)