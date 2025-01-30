from django.urls import path

from insights import views

urlpatterns = [
    # NOTE: This urls handle different forms
    path("", views.CreateInsightView.as_view(), name="insight_create"),
    path("royalfuture/", views.CreateInsightView.as_view(), name="insight_create_royalfuture"),
    path("qatar/", views.CreateInsightView.as_view(), name="insight_create_qatar"),
    path("list/", views.InsightListView.as_view(), name="insight_list"),
    path("export-insights/", views.export_insights, name="export_insights"),
]
