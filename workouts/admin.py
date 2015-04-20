from django.contrib import admin

# import from app
from workouts.models import WorkoutDefinition, AssignedWorkout, AssignedWorkoutDate, ExerciseType, ExerciseResult, \
    Exercise


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
#
#
# class ExerciseResultAdmin(admin.ModelAdmin):
#     list_display = ('time', 'rounds', 'assigned_workout', 'note')

class AssignedWokoutDateInline(admin.StackedInline):
    model = AssignedWorkoutDate
    extra = 1
    classes = ('collapse open',)
    inline_classes = ('collapse open',)


class AssignedWorkoutAdmin(admin.ModelAdmin):
    inlines = [
        AssignedWokoutDateInline,
    ]

admin.site.register(ExerciseType)
admin.site.register(WorkoutDefinition)
admin.site.register(AssignedWorkout, AssignedWorkoutAdmin)
# admin.site.register(AssignedWorkoutDate)
admin.site.register(ExerciseResult)
admin.site.register(Exercise)
