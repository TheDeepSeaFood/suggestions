from django.contrib import admin
from insights.models import Insight, Brand, Branch, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "related_department", "created_at")
    list_filter = ("department", "related_department", "created_at")
    search_fields = ("name", "feedback_or_suggestion")
    ordering = ("name",)
    fields = (
        "name",
        "branch",
        "department",
        "related_department",
        "feedback_or_suggestion",
        "image",
        "created_at",
    )

    def get_queryset(self, request):
        # Customize queryset to display Insights in ascending order of name
        query_set = super().get_queryset(request)
        return query_set.order_by("name")
