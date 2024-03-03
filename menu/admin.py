from django.contrib import admin
from .models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'category', 'price', 'availability')

    search_fields = ('name', 'category', 'cuisine_type')

    list_filter = ('category', 'availability', 'cuisine_type')

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
