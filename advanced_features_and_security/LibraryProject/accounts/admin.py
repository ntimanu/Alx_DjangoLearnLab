from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model
    """
    # Fields to display in the changelist
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    
    # Fields for filtering users in the admin
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    # Search fields for the admin search bar
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Fields to display when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    # Fields to display when editing an existing user, with custom fields added
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

# Register the model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)