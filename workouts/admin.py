from django.contrib import admin
from django import forms
from django.db.models import *
from tinymce.widgets import TinyMCE

# import from app
from workouts.models import WorkoutDefinition, AssignedWorkout, AssignedWorkoutDate, WorkoutType, WorkoutResult, \
    Exercise, PersonalBest

class WorkoutDefinitionForm(forms.ModelForm):
    warmup_content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 15}))
    substitution_content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 15}))
    cooldown_content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 15}))
    extracredit_content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 15}))
    homework_content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 15}))
    class Meta:
        model = WorkoutDefinition


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
    list_display = ('workout_name','get_groups', 'created',)
    inlines = [
        AssignedWokoutDateInline,
    ]

    def get_groups(self, obj):
        return "<br/>".join([p.name for p in obj.workout.assigned_to.all()])
    get_groups.short_description = 'Group List'
    get_groups.allow_tags = True

    def workout_name(self,obj):
        return obj.workout.workout_nick_name
    workout_name.short_description = 'Workout Name'

admin.site.register(AssignedWorkout, AssignedWorkoutAdmin)


class WorkoutTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'type_description', 'created',)

admin.site.register(WorkoutType,WorkoutTypeAdmin)

class WorkoutDefinitionAdmin(admin.ModelAdmin):
    form = WorkoutDefinitionForm

    list_display = ('workout_nick_name', 'introduction_header', 'workout_header',
                    'get_workout_content','coach_name','workout_type','get_groups','get_exercises','created',)

    def get_workout_content(self,obj):
        return obj.workout_content
    get_workout_content.short_description = 'Workout Content'
    get_workout_content.allow_tags = True

    def coach_name(self, obj):
        return obj.coach.get_full_name()
    coach_name.short_description = 'Coach Name'

    def get_exercises(self, obj):
        return "<br/>".join([p.exercise_content for p in obj.exercises.all()])
    get_exercises.short_description = 'Exercise List'
    get_exercises.allow_tags = True

    def get_groups(self, obj):
        return "<br/>".join([p.name for p in obj.assigned_to.all()])
    get_groups.short_description = 'Group List'
    get_groups.allow_tags = True

admin.site.register(WorkoutDefinition,WorkoutDefinitionAdmin)


class WorkoutResultAdmin(admin.ModelAdmin):
    list_display = ('workout_name','student_name','time_taken', 'rounds', 'result_submit_date', 'note','result_workout_assign_date',)

    def workout_name(self,obj):
        return obj.result_workout_assign_date.assigned_workout.workout.workout_nick_name
    workout_name.short_description = 'Workout Name'

    def student_name(self,obj):
        return obj.result_workout_assign_date.assigned_workout.student.get_full_name()
    student_name.short_description = 'Student Name'

admin.site.register(WorkoutResult,WorkoutResultAdmin)


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise_content','workout_list',)

    def workout_list(self, obj):
        return "<br/>".join([p.workout_nick_name for p in obj.exercise_workout.all()])
    workout_list.short_description = 'Workout List'
    workout_list.allow_tags = True

admin.site.register(Exercise,ExerciseAdmin)


class PersonalBestAdmin(admin.ModelAdmin):
    list_display = ('student_name','workout_name','workout_type','workout_assign_date',)

    def workout_name(self,obj):
        return obj.workout_assigned_date.assigned_workout.workout.workout_nick_name
    workout_name.short_description = 'Workout Name'

    def workout_type(self,obj):
        return obj.workout_assigned_date.assigned_workout.workout.workout_type
    workout_type.short_description = 'Workout Type'

    def student_name(self,obj):
        return obj.workout_assigned_date.assigned_workout.student.get_full_name()
    student_name.short_description = 'Student Name'

    def workout_assign_date(self,obj):
        return obj.workout_assigned_date.assigned_date.strftime('%Y-%m-%d')
    workout_assign_date.short_description = 'Workout Assigned Date'

admin.site.register(PersonalBest,PersonalBestAdmin)