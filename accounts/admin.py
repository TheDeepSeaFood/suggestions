from django.contrib import admin
from accounts.models import User


@admin.register(User)
class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "user_type",
    )
    list_filter = ("user_type",)
