from django.urls import path

from insights import views

urlpatterns = [
    path("", views.CreateInsightView.as_view(), name="insight_create"),
    path("list/", views.InsightListView.as_view(), name="insight_list"),
    path("export-insights/", views.export_insights, name="export_insights"),
]
