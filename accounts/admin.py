from django.contrib import admin
from accounts.admin_forms import UserChangeForm, UserCreationForm
from accounts.models import AppUser, AppCoach, AppStudent, ContactUs, UserSubscription, FitnessAppStudent

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

User = get_user_model()

class StudentInline(admin.StackedInline):
    model = AppStudent
    can_delete = False
    verbose_name_plural = 'Student'

class CoachInline(admin.StackedInline):
    model = AppCoach
    can_delete = False
    verbose_name_plural = 'Coach'

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'email', 'is_active','user_role',)
#     fieldsets = (
#         ('Fitness Application User', {
#          'fields': ('first_name', 'last_name', 'email', 'password', 'is_active','user_role')}),
#     )
#     # inlines = [StudentInline,]

# Define a new User admin
# class StudentAdmin(FitnessAppUser):
#     inlines = (StudentInline, )
#
# # Define a new User admin
# class CoachAdmin(admin.ModelAdmin):
#     inlines = (CoachInline, )

# admin.site.register(FitnessAppUser, StudentAdmin)
# admin.site.register(FitnessAppUser, CoachAdmin)

admin.site.register(ContactUs)

class GroupAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                           widget=FilteredSelectMultiple('Users', False),
                                           required=False)
    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            initial = kwargs.get('initial', {})
            initial['users'] = instance.user_set.all()
            kwargs['initial'] = initial
        super(GroupAdminForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        group = super(GroupAdminForm, self).save(commit=commit)

        if commit:
            group.user_set = self.cleaned_data['users']
        else:
            old_save_m2m = self.save_m2m
            def new_save_m2m():
                old_save_m2m()
                group.user_set = self.cleaned_data['users']
            self.save_m2m = new_save_m2m
        return group

class MyGroupAdmin(GroupAdmin):
    form = GroupAdminForm

admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)

class StudentAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'email', 'first_name', 'last_name', 'user_role')
    list_filter = ()
    fieldsets = (
        ('Student', {
         'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('User Type', {'fields': ('user_role',)}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        ('Add Fitness App Student', {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_active',
                       'user_role')}
         ),
        # ('Student Subscription', {
        #     'classes': ('wide',),
        #     'fields': ('subscription', 'parse_installation_id', 'apple_subscription_id')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def get_queryset(self, request):
        return super(StudentAdmin, self).get_queryset(request).filter(user_role=AppUser.User)

admin.site.register(FitnessAppStudent, StudentAdmin)
