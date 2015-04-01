from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts.models import AppCoach, AppUser, DefinedWorkOut, AssignedWorkOut
from accounts.admin_forms import UserCreationForm
# Register your models here.


class childinline(admin.TabularInline):
    model = AppCoach


class CoachAdmin(admin.ModelAdmin):
    # fields = ['email', 'first_name', 'last_name' ]
    fieldsets = (
        ('App User', {
         'fields': ('email', 'first_name', 'password')}),
    )

    inlines = [ childinline]


class WorkOutAdmin(admin.ModelAdmin):
    # fields = ['defined_work_out', 'defined_work_out_title', 'coach_defined_workout' ]
    fieldsets = (
        ('Workouts', {
         'fields': ('defined_work_out', 'defined_work_out_title', 'coach_defined_workout')}),
    )


class AssignedWorkOutAdmin(admin.ModelAdmin):
    fieldsets = (
        ('AssignedWorkOut', {
         'fields': ('student_assigned_workout' , 'defined_work_out_id', 'assigned_date',)}),
    )


admin.site.register(AppUser, CoachAdmin)
admin.site.register(DefinedWorkOut, WorkOutAdmin)
admin.site.register(AssignedWorkOut, AssignedWorkOutAdmin)
