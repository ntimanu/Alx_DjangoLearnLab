from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')

def create_groups():
    """
    Function to create groups and assign permissions automatically.
    Run this once after migrations.
    """
    content_type = ContentType.objects.get_for_model(Book)

    # Create groups if they don’t exist
    admins_group, _ = Group.objects.get_or_create(name="Admins")
    editors_group, _ = Group.objects.get_or_create(name="Editors")
    viewers_group, _ = Group.objects.get_or_create(name="Viewers")

    # Assign permissions to groups
    view_permission = Permission.objects.get(codename="can_view", content_type=content_type)
    create_permission = Permission.objects.get(codename="can_create", content_type=content_type)
    edit_permission = Permission.objects.get(codename="can_edit", content_type=content_type)
    delete_permission = Permission.objects.get(codename="can_delete", content_type=content_type)

    # Assign permissions
    admins_group.permissions.set([view_permission, create_permission, edit_permission, delete_permission])
    editors_group.permissions.set([view_permission, create_permission, edit_permission])
    viewers_group.permissions.set([view_permission])

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'date_of_birth', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'date_of_birth', 'profile_photo', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
