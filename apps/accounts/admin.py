from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'full_name', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'full_name', 'email')
    ordering = ('role', 'username')

    fieldsets = UserAdmin.fieldsets + (
        ("Qo'shimcha ma'lumot", {'fields': ('role', 'full_name')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Qo'shimcha ma'lumot", {'fields': ('role', 'full_name', 'email')}),
    )

    # O'zbek tilida sarlavhalar
    def has_add_permission(self, request):
        return super().has_add_permission(request)

    class Media:
        pass