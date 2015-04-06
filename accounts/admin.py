from django.contrib import admin

from accounts.models import AppUser, AppCoach
from work_outs.models import WorkOutDefinition, AssignedWorkOut, WorkOutType

class childinline(admin.TabularInline):
    model = AppCoach


class CoachAdmin(admin.ModelAdmin):
    fieldsets = (
        ('App User', {
         'fields': ('email', 'first_name', 'password')}),
    )

    inlines = [ childinline]


class WorkOutAdmin(admin.ModelAdmin):
    fieldsets = (
        ('WorkoutDefinitions', {
         'fields': ('defined_work_out_title', 'defined_work_out_text', 'coach_defined_workout', 'workout_type',)}),
    )


class WorkOutTypesAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Workout Types', {
         'fields': ('workout_type',)}),
    )


class AssignedWorkOutAdmin(admin.ModelAdmin):
    fieldsets = (
        ('AssignedWorkOut', {
         'fields': ('student_assigned_workout', 'defined_work_out_id', 'assigned_date',)}),
    )


admin.site.register(AppUser, CoachAdmin)
admin.site.register(WorkOutType, WorkOutTypesAdmin)
admin.site.register(WorkOutDefinition, WorkOutAdmin)
admin.site.register(AssignedWorkOut, AssignedWorkOutAdmin)
