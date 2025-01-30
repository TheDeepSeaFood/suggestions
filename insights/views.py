import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, View

from insights.models import Branch, Department, Insight
from insights.utils import export_insights_to_excel

logger = logging.getLogger("django")


def create_insight(
    name,
    department,
    feedback_suggestions,
    fileupload=None,
    type=None,
    branch_id=None,
    related_department_id=None,
):
    """
    Function to create an Insight instance.

    Args:
        name (str): Name of the person providing feedback.
        department (str): Department of the person providing feedback.
        feedback_suggestions (str): The feedback or suggestion text.
        fileupload (File, optional): Uploaded file (image). Defaults to None.
        branch_id (int, optional): ID of the branch. Defaults to None.
        related_department_id (int, optional): ID of the related department. Defaults to None.

    Returns:
        tuple: (success: bool, messages: list)
    """
    errors = []
    branch = None
    related_department = None

    # Validation
    if not name:
        errors.append("Name is required.")
    if not department:
        errors.append("Department is required.")
    if not feedback_suggestions:
        errors.append("Feedback/Suggestions is required.")

    if fileupload:
        if fileupload.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            errors.append("File must be an image of type .jpg, .jpeg or .png.")
        if fileupload.size > 5 * 1024 * 1024:  # 5MB
            errors.append("File size cannot exceed 5 MB.")

    if branch_id:
        try:
            branch = Branch.objects.get(id=branch_id)
        except ObjectDoesNotExist:
            errors.append("Invalid branch selected.")

    if related_department_id:
        try:
            related_department = Department.objects.get(id=related_department_id)
        except ObjectDoesNotExist:
            errors.append("Invalid related department selected.")

    # Validate type
    allowed_types = ["DSF", "ROF", "QAR"]
    if type not in allowed_types:
        type = "DSF"  # Default value if invalid

    # If there are errors, return failure status with messages
    if errors:
        return False, errors

    # Save to database
    try:
        Insight.objects.create(
            name=name,
            branch=branch,
            department=department,
            feedback_or_suggestion=feedback_suggestions,
            related_department=related_department,
            image=fileupload,
            type=type,
        )
        return True, ["Your Feedback/Suggestion has been recorded successfully."]
    except Exception as e:
        return False, [f"An error occurred: {e}"]


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
    ordering = ["-created_at"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "List Insights"
        return context


def export_insights(request):
    if request.method == "GET":
        response = export_insights_to_excel()
        return response
    return HttpResponseBadRequest("Invalid request method")
