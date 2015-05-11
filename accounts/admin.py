from django.contrib import admin
from accounts.models import AppUser, AppCoach, AppStudent, ContactUs


class StudentInline(admin.TabularInline):
    model = AppStudent


class StudentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Fitness Application Student', {
         'fields': ('first_name', 'last_name', 'email', 'password', 'is_active','user_role')}),
    )
    inlines = [StudentInline]

admin.site.register(AppCoach)
admin.site.register(AppUser, StudentAdmin)
admin.site.register(ContactUs)


# class AppStudentInline(admin.StackedInline):
#     model = AppStudent
#     extra = 1
#     classes = ('collapse open',)
#     inline_classes = ('collapse open',)
#
# class AppStudentAdmin(admin.ModelAdmin):
#     inlines = [
#         AppStudentInline,
#     ]
#
#
# admin.site.register(AppUser, AppStudentAdmin)
