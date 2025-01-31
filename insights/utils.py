import openpyxl
from django.http import HttpResponse
from insights.models import Insight, Branch, Department
from django.core.exceptions import ObjectDoesNotExist


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
    allowed_types = ["DSF", "ROF", "QAR", "AIN", "ABD"]

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
            if branch.name == "Abu Dhabi":
                type = "ABD"
            elif branch.name == "Al Ain":
                type = "AIN"
        except ObjectDoesNotExist:
            errors.append("Invalid branch selected.")

    if related_department_id:
        try:
            related_department = Department.objects.get(id=related_department_id)
        except ObjectDoesNotExist:
            errors.append("Invalid related department selected.")

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
