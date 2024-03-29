from django.conf.urls import url, include, patterns

from api.views import AssignedWorkoutViewSet, SubscriptionViewSet, ResultViewSet, workout_result, personal_best, \
    ContactUsViewSet,leader_board

urlpatterns = patterns('',
    url(r'^workout/$', AssignedWorkoutViewSet.as_view()),
    url(r'workout/result/$', workout_result),
    url(r'workout/personal-best/$', personal_best),
    url(r'workout/leader-board/$', leader_board),
    url(r'^exercise/result/$', ResultViewSet.as_view({'post': 'create', 'put': 'update', 'get': 'list'})),
    url(r'^subscription/$', SubscriptionViewSet.as_view({'get': 'get'})),
    url(r'^contact-us/$', ContactUsViewSet.as_view({'post': 'create'})),

)

