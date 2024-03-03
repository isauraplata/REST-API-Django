from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = ('id', 'full_name', 'email', 'position', 'salary', 'is_active')

    search_fields = ('first_name', 'last_name', 'email')

    list_filter = ('position', 'is_active')

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
