# modules/cv_generator.py

from templates.template1 import render_template1
import tempfile


def generate_cv_pdf(user_data: dict):
    """
    Generate CV PDF using Classic template only.
    Returns the path to a temporary PDF file.
    """

    # Get color (optional)
    color = user_data.get("color", "#000000")

    # Generate PDF using ONLY Classic template
    pdf = render_template1(user_data, color)

    # Save PDF to temporary file
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)
    temp_pdf.close()

    return temp_pdf.name