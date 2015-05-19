from django.contrib import admin
from accounts.models import AppUser, AppCoach, AppStudent, ContactUs


class StudentInline(admin.TabularInline):
    model = AppStudent
    fieldsets = (
        ('Fitness Application Student Subscription', {
         'fields': ('subscription', )}),
    )

# admin.site.register(AppCoach)
# admin.site.register(AppUser, StudentAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_active','user_role',)
    fieldsets = (
        ('Fitness Application User', {
         'fields': ('first_name', 'last_name', 'email', 'password', 'is_active','user_role')}),
    )
    inlines = [StudentInline,]

admin.site.register(AppUser, UserAdmin)

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
