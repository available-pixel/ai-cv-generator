from fpdf import FPDF
from utils.text_cleaner import clean_text
import os

def render_template1(user_data, hex_color="#000000"):
    pdf = FPDF(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ================= FONTS =================
    # Get folder where this file is
    BASE_DIR = os.path.dirname(__file__)
    FONT_DIR = os.path.join(BASE_DIR, "../dejavu-sans")  # adjust "../" if your modules folder is nested differently

    pdf.add_font('DejaVu', '', os.path.join(FONT_DIR, 'DejaVuSans.ttf'), uni=True)
    pdf.add_font('DejaVu', 'B', os.path.join(FONT_DIR, 'DejaVuSans-Bold.ttf'), uni=True)
    pdf.add_font('DejaVu', 'I', os.path.join(FONT_DIR, 'DejaVuSans-Oblique.ttf'), uni=True)
    pdf.add_font('DejaVu', 'BI', os.path.join(FONT_DIR, 'DejaVuSans-BoldOblique.ttf'), uni=True)

    # Color
    r, g, b = tuple(int(hex_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    LEFT_MARGIN = 15
    RIGHT_MARGIN = 195
    WIDTH = RIGHT_MARGIN - LEFT_MARGIN

    # ================= HEADER =================
    pdf.set_text_color(r, g, b)
    pdf.set_font("DejaVu", "B", 18)
    pdf.cell(0, 10, user_data.get("name", ""), ln=True)

    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(0, 0, 0)

    contact = " | ".join(filter(None, [
        user_data.get("email"),
        user_data.get("phone"),
        user_data.get("location")
    ]))
    if contact:
        pdf.set_x(LEFT_MARGIN)
        pdf.multi_cell(WIDTH, 6, contact)

    links = " | ".join(filter(None, [
        user_data.get("linkedin"),
        user_data.get("github"),
        user_data.get("website")
    ]))
    if links:
        pdf.set_x(LEFT_MARGIN)
        pdf.multi_cell(WIDTH, 6, links)

    pdf.ln(3)

    # ================= PROFILE PHOTO =================
    profile_photo = user_data.get("profile_photo")
    if profile_photo:
        # Move pointer to start
        profile_photo.seek(0)
        # Place image top-right corner
        pdf.image(profile_photo, x=180, y=5, w=20, h=0)  # adjust position & size as needed

    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(0, 0, 0)

    # ================= LINE =================
    pdf.set_draw_color(r, g, b)
    pdf.set_line_width(0.8)
    pdf.line(11.5, pdf.get_y(), RIGHT_MARGIN, pdf.get_y())
    pdf.ln(5)

    # ================= PROFILE =================
    profile = user_data.get("profile")
    if profile and profile.strip():
        section_title(pdf, "PROFILE", r, g, b)
        pdf.set_font("DejaVu", "", 11)
        pdf.multi_cell(WIDTH, 6, clean_text(profile))
        pdf.ln(2)

    # ================= RESEARCH =================
    research = user_data.get("research", [])
    valid_research = [r for r in research if any(r.values())]

    if valid_research:
        section_title(pdf, "RESEARCH", r, g, b)
        for res in valid_research:
            pdf.set_font("DejaVu", "B", 11)
            pdf.set_x(10)
            pdf.cell(0, 6, res.get("title", ""), ln=True)

            if res.get("description"):
                pdf.set_font("DejaVu", "", 11)
                pdf.set_x(LEFT_MARGIN)
                pdf.multi_cell(WIDTH, 5, clean_text(res.get("description")))

            other_info = " | ".join(filter(None, [res.get("publication"), res.get("link")]))
            if other_info:
                pdf.set_font("DejaVu", "I", 10)
                pdf.set_x(LEFT_MARGIN)
                for part in other_info.split("|"):
                    part = part.strip()
                    if part.startswith("http"):
                        pdf.cell(0, 5, part, ln=True, link=part)
                    else:
                        pdf.cell(0, 5, part, ln=True)
            pdf.ln(2)

    # ================= PROJECTS =================
    projects = user_data.get("projects", [])
    valid_projects = [p for p in projects if any(p.values())]

    if valid_projects:
        section_title(pdf, "PROJECTS", r, g, b)
        for proj in valid_projects:
            pdf.set_font("DejaVu", "B", 11)
            pdf.set_x(10)
            pdf.cell(0, 6, proj.get("name", ""), ln=True)

            if proj.get("description"):
                pdf.set_font("DejaVu", "", 11)
                pdf.set_x(12)
                pdf.multi_cell(WIDTH, 5, clean_text(proj.get("description")))

            if proj.get("technologies"):
                pdf.set_x(12)
                pdf.set_font("DejaVu", "B", 10)
                pdf.cell(12, 5, "Tech:")
                pdf.set_font("DejaVu", "I", 10)
                pdf.multi_cell(WIDTH - 12, 5, proj.get("technologies"))

            links = [l for l in proj.get("links", []) if l.strip()]

            if links:
                pdf.set_x(12)
                pdf.set_font("DejaVu", "B", 10)
                pdf.cell(12, 5, "Links:")
                start_x = pdf.get_x()
                pdf.set_font("DejaVu", "I", 10)

                for i, link in enumerate(links):
                    text = link + (" | " if i < len(links) - 1 else "")
                    text_width = pdf.get_string_width(text)

                    if pdf.get_x() + text_width > RIGHT_MARGIN:
                        pdf.ln(5)
                        pdf.set_x(start_x)

                    pdf.cell(text_width, 5, text, link=link)

            pdf.ln(6)

    # ================= SKILLS =================
    skills = user_data.get("skills")
    if skills and skills.strip():
        section_title(pdf, "SKILLS", r, g, b)
        pdf.set_font("DejaVu", "", 11)
        pdf.multi_cell(WIDTH, 6, skills)
        pdf.ln(2)

        # ================= CERTIFICATIONS =================
        certifications = user_data.get("certifications", [])
        valid_certifications = [c for c in certifications if any(c.values())]

        if valid_certifications:
            section_title(pdf, "CERTIFICATIONS", r, g, b)

            for cert in valid_certifications:
                pdf.set_font("DejaVu", "B", 11)
                pdf.set_x(10)
                pdf.cell(0, 6, cert.get("name", ""), ln=True)

                if cert.get("link"):
                    pdf.set_font("DejaVu", "I", 10)
                    pdf.set_x(12)
                    pdf.cell(0, 5, cert.get("link"), ln=True, link=cert.get("link"))

                pdf.ln(2)

    # ================= LANGUAGES =================
    languages = user_data.get("languages", [])
    valid_languages = [l for l in languages if l.get("language")]

    if valid_languages:
        section_title(pdf, "LANGUAGES", r, g, b)
        for lang in valid_languages:
            pdf.set_x(12)
            pdf.set_font("DejaVu", "B", 11)
            pdf.cell(30, 5, lang.get("language", ""))
            pdf.set_font("DejaVu", "", 11)
            pdf.cell(0, 5, lang.get("level", ""), ln=True)
        pdf.ln(2)

    # ================= EDUCATION =================
    education = user_data.get("education", [])
    valid_education = [e for e in education if any(e.values())]

    if valid_education:
        section_title(pdf, "EDUCATION", r, g, b)

        for edu in valid_education:
            pdf.set_font("DejaVu", "B", 11)
            pdf.set_x(10)
            pdf.cell(0, 6, edu.get("degree", ""), ln=True)

            info = " | ".join(filter(None, [
                edu.get("school"),
                edu.get("year")
            ]))

            if info:
                pdf.set_font("DejaVu", "I", 10)
                pdf.set_x(12)
                pdf.multi_cell(WIDTH, 5, info)

            pdf.ln(2)

    # ================= EXPERIENCE =================
    experience = user_data.get("experience", [])
    valid_experience = [e for e in experience if any(e.values())]

    if valid_experience:
        section_title(pdf, "EXPERIENCE", r, g, b)
        for exp in valid_experience:
            pdf.set_font("DejaVu", "B", 11)
            pdf.set_x(10)
            pdf.cell(0, 6, exp.get("job", ""), ln=True)

            info = " | ".join(filter(None, [exp.get("company"), exp.get("duration")]))
            if info:
                pdf.set_font("DejaVu", "I", 10)
                pdf.set_x(12)
                pdf.multi_cell(WIDTH, 5, info)

            if exp.get("description"):
                pdf.set_font("DejaVu", "", 11)
                pdf.set_x(12)
                pdf.multi_cell(WIDTH, 5, clean_text(exp.get("description")))

            pdf.ln(2)

    return pdf


# ================= HELPER =================
def section_title(pdf, title, r, g, b):
    pdf.set_text_color(r, g, b)
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 7, title, ln=True)
    pdf.set_draw_color(r, g, b)
    pdf.set_line_width(0.4)
    pdf.line(11.5, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(2)
    pdf.set_text_color(0, 0, 0)