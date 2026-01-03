from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import re


def normalize_cover_body(text: str) -> str:
    """
    Enforce BODY-ONLY content from LLM output.
    Removes markdown, headers, greetings, links, and contact info.
    """

    # Remove markdown (**bold**, *italic*)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)

    # Remove markdown links [text](url)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    forbidden = [
        r"^hamza\s+mohsin.*$",
        r".*@.*",                      # email
        r"\+?\d[\d\s\-]{6,}",           # phone
        r"linkedin\.com.*",
        r"github\.com.*",
        r"portfolio.*",
        r"^date.*$",
        r"^hiring manager.*$",
    ]

    lines = []
    for line in text.splitlines():
        l = line.strip()
        if not l:
            lines.append("")
            continue

        if any(re.search(p, l.lower()) for p in forbidden):
            continue

        if l.lower().startswith(("dear ", "kind regards", "best regards", "sincerely")):
            continue

        lines.append(l)

    cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def draw_wrapped_paragraph(c, text, x, y, width):
    style = ParagraphStyle(
        name="CoverBody",
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        spaceAfter=12,
    )
    p = Paragraph(text.replace("\n", "<br/>"), style)
    w, h = p.wrap(width, 800)
    p.drawOn(c, x, y - h)
    return y - h


def save_cover_letter_pdf(
    filename: str,
    applicant_name: str,
    job_title: str,
    company: str,
    body_text: str
):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    x = 2.5 * cm
    y = height - 2.5 * cm

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y, "Cover Letter")
    y -= 2 * cm

    # Subject
    c.setFont("Helvetica-Bold", 11)
    c.drawString(
        x,
        y,
        f"Subject: Application for {job_title} – {company}"
    )
    y -= 1.5 * cm

    # Greeting
    c.setFont("Helvetica", 11)
    c.drawString(x, y, "Dear Hiring Manager,")
    y -= 1.2 * cm

    # Clean + wrap body
    clean_body = normalize_cover_body(body_text)
    usable_width = width - (2 * x)
    y = draw_wrapped_paragraph(c, clean_body, x, y, usable_width)

    # Closing
    y -= 1.5 * cm
    c.setFont("Helvetica", 11)
    c.drawString(x, y, "Kind regards,")
    y -= 1 * cm
    c.drawString(x, y, applicant_name)

    c.showPage()
    c.save()
