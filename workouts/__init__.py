from django.apps import AppConfig

EXERCISE_TYPE_TIME = 'Time'
EXERCISE_TYPE_ROUNDS = 'Rounds'


class WorkOutAppConfig(AppConfig):
    name = 'workouts'

    def ready(self):
        """
        initializing Constants and creating fields in db if they do not exist already.
        """
        try:
            from workouts.models import ExerciseType
            from workouts import EXERCISE_TYPE_ROUNDS, EXERCISE_TYPE_TIME
            exercise_type_time = ExerciseType.objects.get_or_create(type_name=EXERCISE_TYPE_TIME)
            exercise_type_rounds = ExerciseType.objects.get_or_create(type_name=EXERCISE_TYPE_ROUNDS)
        except Exception:
            pass

default_app_config = 'workouts.WorkOutAppConfig'