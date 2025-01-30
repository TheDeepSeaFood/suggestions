import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, View

from insights.models import Branch, Department, Insight
from insights.utils import export_insights_to_excel, create_insight

logger = logging.getLogger("django")


class CreateInsightView(View):
    template_name = "insights/create_insight.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "page_title": "Suggestions/Feedback",
                "branches": Branch.objects.all(),
                "departments": Department.objects.all(),
            },
        )

    def post(self, request):
        type_value = request.POST.get("type")
        success, response_messages = create_insight(
            name=request.POST.get("name"),
            department=request.POST.get("department"),
            feedback_suggestions=request.POST.get("feedback-suggestions"),
            fileupload=request.FILES.get("fileupload"),
            branch_id=request.POST.get("branch"),
            related_department_id=request.POST.get("related_department"),
            type=type_value,
        )

        # Add messages based on response
        for message in response_messages:
            messages.add_message(
                request, messages.SUCCESS if success else messages.ERROR, message
            )

        # Redirect on success or reload the form on failure
        if success:
            if type_value == "ROF":
                return redirect(reverse_lazy("insight_create_royalfuture"))
            elif type_value == "QAR":
                return redirect(reverse_lazy("insight_create_qatar"))
            else:
                return redirect(reverse_lazy("insight_create"))

        return self.get(request)


class InsightListView(LoginRequiredMixin, ListView):
    model = Insight
    template_name = "insights/list_insights.html"
    context_object_name = "insights"
    paginate_by = 10

    def get_queryset(self):
        """Filter insights based on the logged-in user's user_type."""
        user = self.request.user

        if user.is_superuser:
            return Insight.objects.all().order_by("-created_at")

        # NOTE : Filter the insights on the user_type so that the designated user is the
        # only one who can view there insights
        return Insight.objects.filter(type=user.user_type).order_by("-created_at")


def export_insights(request):
    if request.method == "GET":
        response = export_insights_to_excel()
        return response
    return HttpResponseBadRequest("Invalid request method")
