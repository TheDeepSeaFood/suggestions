from django.db import models
from django.utils import timezone


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"


class Insight(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, null=True, on_delete=models.SET_NULL)
    department = models.CharField(max_length=100)
    feedback_or_suggestion = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to="insight_images")
    related_department = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Feedback And Suggestion"
        verbose_name_plural = "Feedbacks And Suggestions"
        ordering = ["department"]
