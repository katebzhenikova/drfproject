from django.contrib import admin

from material.models import Course, Subscription
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'city', 'is_active', 'is_staff')
    search_fields = ('email', 'phone')
    list_filter = ('is_active', 'is_staff', 'city', 'groups')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'city', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2'),
        }),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')
    search_fields = ('is_subscribed', 'title')
    list_filter = ('title', 'id')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'is_subscribed')
    search_fields = ('user', 'course', 'is_subscribed')
    list_filter = ('user', 'course', 'is_subscribed')
