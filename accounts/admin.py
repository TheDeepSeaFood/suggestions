from django.contrib import admin
from accounts.models import User


@admin.register(User)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("username", "branch", "brand")
    search_fields = ("username", "branch", "brand")
