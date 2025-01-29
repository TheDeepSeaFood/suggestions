import openpyxl
from django.http import HttpResponse
from insights.models import Insight


def export_insights_to_excel():
    # Create a new workbook and select the active worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Insights"

    # Define the column headers
    headers = [
        "Name",
        "Branch",
        "Department",
        "Feedback or Suggestion",
        "Related Department",
        "Created At",
    ]
    worksheet.append(headers)

    # Fetch all instances of the Insight model
    insights = Insight.objects.all()

    # Loop through each insight and add it to the worksheet
    for insight in insights:
        row = [
            insight.name,
            insight.branch.name if insight.branch else "",
            insight.department,
            insight.feedback_or_suggestion,
            insight.related_department.name if insight.related_department else "",
            insight.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        ]
        worksheet.append(row)

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="insights.xlsx"'

    # Save the workbook to the response
    workbook.save(response)

    return response
