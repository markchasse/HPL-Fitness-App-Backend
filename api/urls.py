from django.conf.urls import url, include, patterns

from api.views import AssignedWorkoutViewSet, SubscriptionViewSet, ResultViewSet

urlpatterns = patterns('',
    url(r'^workout/$', AssignedWorkoutViewSet.as_view()),

    url(r'^exercise/result/$', ResultViewSet.as_view({'post': 'create', 'put': 'update'})),
    # url(r'^exercise/result/$', ResultViewSet.as_view({'post': 'create', 'put': 'update'})),
    url(r'^subscription/$', SubscriptionViewSet.as_view({'get': 'get'})),

)

