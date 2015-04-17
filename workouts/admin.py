from django.contrib import admin

# import from app
from workouts.models import WorkoutDefinition, AssignedWorkout, ExerciseType, ExerciseResult, Exercise


# class WorkoutAdmin(admin.ModelAdmin):
#     list_display = ('introduction_header', 'introduction_textfield', 'warmup_header', 'warmup_content',
#                     'warmup_notes', 'substitution_header', 'substitution_content', 'substitution_notes',
#                     'cooldown_header', 'cooldown_content', 'cooldown_notes', 'extracredit_header',
#                     'extracredit_content', 'extracredit_notes', 'homework_header', 'homework_content',
#                     'homework_notes', 'coach')
#     list_filter = ('coach',)
#
#     fieldsets = (
#         ('Workout Definitions',
#          {
#          'fields': ('introduction_header', 'introduction_textfield', 'warmup_header', 'warmup_content',
#                     'warmup_notes', 'substitution_header', 'substitution_content', 'substitution_notes',
#                     'cooldown_header', 'cooldown_content', 'cooldown_notes', 'extracredit_header',
#                     'extracredit_content', 'extracredit_notes', 'homework_header', 'homework_content',
#                     'homework_notes', 'coach')
#         }),
#     )
#
#
# class ExerciseTypesAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     fieldsets = (
#         ('Workout Types', {
#          'fields': ('name', 'description')}),
#     )
#
# class ExceriseAdmin(admin.ModelAdmin):
#     list_display = ('workout_header', 'workout', 'workout_content', 'workout_notes', 'workout_type')
#     fieldsets = (
#         ('Excersie', {
#          'fields': ('workout_header','workout', 'workout_content', 'workout_notes','workout_type')}),
#     )
#
# class AssignedWorkoutAdmin(admin.ModelAdmin):
#     list_display = ('student', 'workout', 'assigned_date',)
#     fieldsets = (
#         ('Assigned Workout', {
#          'fields': ('student', 'workout', 'assigned_date',)}),
#     )
#
#
# class ExerciseResultAdmin(admin.ModelAdmin):
#     list_display = ('time', 'rounds', 'assigned_workout', 'note')


admin.site.register(ExerciseType)
admin.site.register(WorkoutDefinition)
admin.site.register(AssignedWorkout)
admin.site.register(ExerciseResult)
admin.site.register(Exercise)
