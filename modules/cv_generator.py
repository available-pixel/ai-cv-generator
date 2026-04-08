# modules/cv_generator.py
from templates.template1 import render_template1
import tempfile

def generate_cv_pdf(user_data: dict, return_bytes: bool = False):
    """
    Generate CV PDF using Classic template.
    Returns path to temporary PDF file OR bytes (if return_bytes=True)
    """

    # Get color (optional)
    color = user_data.get("color", "#000000")

    # Generate PDF
    pdf = render_template1(user_data, color)

    if return_bytes:
        pdf_output = pdf.output(dest='S')

        # ✅ FIX: handle both str and bytes
        if isinstance(pdf_output, str):
            return pdf_output.encode('latin1')
        else:
            return bytes(pdf_output)

    else:
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(temp_pdf.name)
        temp_pdf.close()
        return temp_pdf.name