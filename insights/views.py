import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from insights.forms import InsightForm
from insights.models import Insight

logger = logging.getLogger("django")


class InsightCreateView(CreateView):
    model = Insight
    form_class = InsightForm
    template_name = "insights/create_insight.html"
    success_url = reverse_lazy("insight_create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Suggestions/Feedback"
        return context

    def form_valid(self, form):
        messages.success(
            self.request, "Your Feedback/Suggestion has been recoded successfully"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for error_list in form.errors.values():
            for errors in error_list:
                messages.error(self.request, errors, extra_tags="alert-danger")
        return super().form_invalid(form)
