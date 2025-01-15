from django.contrib import admin
from insights.models import Insight, Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "related_department")
    list_filter = ("department", "related_department")
    search_fields = ("name", "feedback_or_suggestion")
    ordering = ("name",)
    fields = ("name", "department", "related_department", "feedback_or_suggestion")

    def get_queryset(self, request):
        # Customize queryset to display Insights in ascending order of name
        query_set = super().get_queryset(request)
        return query_set.order_by("name")
