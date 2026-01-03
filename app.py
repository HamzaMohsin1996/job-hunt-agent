from dotenv import load_dotenv
load_dotenv()

import gradio as gr
import tempfile
import os

from graph.workflow import build_graph
from graph.state import JobHuntState
from utils.io_helpers import extract_cv_text, fetch_job_text
from utils.pdf_export import save_cover_letter_pdf

# ============================================================
# Build LangGraph app
# ============================================================
app = build_graph()


def run(cv_pdf, job_url, task, model_name, feedback, satisfied):
    # ================= SAFETY CHECKS =================
    if cv_pdf is None:
        return "❌ Please upload your CV (PDF).", None

    if not job_url.strip():
        return "❌ Please provide a job posting URL.", None

    # Normalize model name (extra safety)
    if model_name == "llama3.1":
        model_name = "ollama:llama3.1"

    # ================= EXTRACT CV =================
    try:
        cv_text = extract_cv_text(cv_pdf.name)
    except Exception as e:
        return f"❌ Failed to read CV PDF: {e}", None

    # ================= FETCH JOB DESCRIPTION =================
    job_description = fetch_job_text(job_url)
    if not job_description.strip():
        return "❌ Could not fetch job description from the URL.", None

    # ================= BUILD STATE =================
    state = JobHuntState(
        cv_text=cv_text,
        job_title="Auto-detected",
        job_description=job_description,
        task=task,
        model_name=model_name,   # 🔑 model selector
        feedback=feedback,
        satisfied=satisfied
    )

    # ================= RUN LANGGRAPH =================
    result = app.invoke(state)

    # ================= NORMALIZE OUTPUT =================
    if isinstance(result, JobHuntState):
        result_dict = {
            "cover_letter": result.cover_letter,
            "networking": result.networking,
            "review": result.review,
        }
    else:
        result_dict = result

    # ================= COVER LETTER =================
    if task == "cover":
        cover_text = result_dict.get("cover_letter", "")
        if not cover_text:
            return "❌ Cover letter generation failed.", None

        pdf_path = os.path.join(
            tempfile.gettempdir(),
            "Hamza_Mohsin_Cover_Letter.pdf"
        )

        save_cover_letter_pdf(
            filename=pdf_path,
            applicant_name="Hamza Mohsin",
            job_title="Auto-detected",
            company="Auto-detected",
            body_text=cover_text
        )

        return cover_text, pdf_path

    # ================= NETWORKING =================
    if task == "networking":
        networking_data = result_dict.get("networking", {})
        return networking_data.get("text", "❌ No networking output generated."), None

    # ================= REVIEW =================
    if task == "review":
        review_data = result_dict.get("review", {})
        return review_data.get("text", "❌ No review output generated."), None

    return "❌ Unknown task selected.", None


# ============================================================
# Gradio UI
# ============================================================
gr.Interface(
    fn=run,
    inputs=[
        gr.File(
            label="Upload CV (PDF)",
            file_types=[".pdf"]
        ),
        gr.Textbox(
            label="Job Posting URL",
            placeholder="https://company.com/jobs/frontend-engineer"
        ),
        gr.Radio(
            ["cover", "networking", "review"],
            label="Task",
            value="cover"
        ),
        gr.Radio(
            choices=[
                ("GPT-4o Mini (Cloud)", "gpt-4o-mini"),
                ("LLaMA 3.1 (Local via Ollama)", "ollama:llama3.1"),
            ],
            label="Model",
            value="ollama:llama3.1"
        ),
        gr.Textbox(
            label="Feedback (optional)",
            placeholder="e.g. Make it more concise"
        ),
        gr.Checkbox(
            label="Satisfied?"
        )
    ],
    outputs=[
        gr.Textbox(
            label="Output",
            lines=28
        ),
        gr.File(
            label="Download Cover Letter (PDF)"
        )
    ],
    title="AI Job Application Assistant",
    description=(
        "Upload your CV, paste a job URL, select a task, and switch freely "
        "between GPT (cloud) and LLaMA (local)."
    )
).launch()
