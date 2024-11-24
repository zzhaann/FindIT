from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Jobs

@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price', 'creator')
    search_fields = ('title', 'city', 'creator__username')
    list_filter = ('city', 'creator')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "role":
            if not request.user.is_superuser:

                kwargs['choices'] = [choice for choice in CustomUser.ROLE_CHOICES if choice[0] != 'admin']
        return super().formfield_for_choice_field(db_field, request, **kwargs)
