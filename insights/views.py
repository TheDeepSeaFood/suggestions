import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView

from insights.models import Insight

logger = logging.getLogger("django")


def create_insight_view(request):
    page_title = "Suggestions/Feedback"

    if request.method == "POST":
        # Fetching data from the POST request
        name = request.POST.get("name")
        department = request.POST.get("department")
        feedback_suggestions = request.POST.get("feedback-suggestions")
        related_department = request.POST.get("related_department")
        fileupload = request.FILES.get("fileupload")

        # Perform manual validation
        errors = []

        if not name:
            errors.append("Name is required.")
        if not department:
            errors.append("Department is required.")
        if not feedback_suggestions:
            errors.append("Feedback/Suggestions is required.")
        if not related_department:
            errors.append("Related Department is required.")
        if fileupload:
            if fileupload.content_type not in [
                "image/jpeg",
                "image/png",
                "image/jpg",
            ]:
                errors.append("File must be an image of type .jpg, .jpeg or .png.")
            if fileupload.size > 5 * 1024 * 1024:  # 5MB
                errors.append("File size cannot exceed 5 MB.")
        else:
            errors.append("File upload is required.")

        # If errors exist, add them to messages and return
        if errors:
            for error in errors:
                messages.error(request, error, extra_tags="alert-danger")
        else:
            # Save the data to the model
            try:
                Insight.objects.create(
                    name=name,
                    department=department,
                    feedback_or_suggestion=feedback_suggestions,
                    related_department=related_department,
                    image=fileupload,
                )
                messages.success(
                    request, "Your Feedback/Suggestion has been recorded successfully"
                )
                return redirect(reverse_lazy("insight_create"))
            except Exception as e:
                messages.error(
                    request, f"An error occurred: {e}", extra_tags="alert-danger"
                )

    return render(
        request,
        "insights/create_insight.html",
        {"page_title": page_title},
    )


class InsightListView(LoginRequiredMixin, ListView):
    model = Insight
    template_name = "insights/list_insights.html"
    context_object_name = "insights"
    ordering = ["department"]
    paginate_by = 10
