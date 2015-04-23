from django.conf.urls import url, include, patterns

from api.views import AssignedWorkoutViewSet, SubscriptionViewSet, ResultViewSet, workout_result, personal_best

urlpatterns = patterns('',
    url(r'^workout/$', AssignedWorkoutViewSet.as_view()),
    url(r'workout/result/$', workout_result),
    url(r'workout/personal-best/$', personal_best),
    url(r'^exercise/result/$', ResultViewSet.as_view({'post': 'create', 'put': 'update', 'get': 'list'})),
    # url(r'^exercise/result/$', ResultViewSet.as_view({'post': 'create', 'put': 'update'})),
    url(r'^subscription/$', SubscriptionViewSet.as_view({'get': 'get'})),

)

