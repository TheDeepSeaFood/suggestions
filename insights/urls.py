from django.urls import path

from insights import views

urlpatterns = [
    path("", views.InsightCreateView.as_view(), name="insight_create"),
    path("list/", views.InsightListView.as_view(), name="insight_list"),
]
